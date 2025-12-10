"""Utilities to interpret free-form messages into structured preferences."""
from __future__ import annotations

import re
from typing import Any

from app.domain.schemas import ChatRequest, FinancingInput
from app.services.catalog_service import CatalogService

KM_PATTERN = re.compile(r"(\d{1,3})(?:\s*|,|\.)?(\d{3})?\s*(k|mil)?\s*(?:km|kil[oó]metros?)", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"(20\d{2})")
AMOUNT_PATTERN = re.compile(r"\b(\d+[\d,.]*)(?:\s*(k|mil))?\b")
YEARS_TERM_PATTERN = re.compile(r"(\d+)\s*(años|anios|years)", re.IGNORECASE)
ENGANCHE_PATTERN = re.compile(r"enganche|anticipo", re.IGNORECASE)
ALIAS_BRANDS = {
    "vw": "Volkswagen",
    "volks": "Volkswagen",
    "chevy": "Chevrolet",
    "bmw": "BMW",
}
ALIAS_MODELS = {
    "vento": "Vento",
    "vocho": "Sedan",
    "cx5": "CX-5",
}


class MessageParser:
    """Extract preferences and financing details from natural language."""

    def __init__(self, catalog_service: CatalogService) -> None:
        self.catalog_service = catalog_service

    def enrich_request(self, request: ChatRequest) -> ChatRequest:
        data = request.model_dump()
        preferences: dict[str, Any] = dict(data.get("preferences") or {})

        if not preferences.get("make"):
            maybe_make = self._extract_make(request.message)
            if maybe_make:
                preferences["make"] = maybe_make

        if not preferences.get("model"):
            maybe_model = self._extract_model(request.message, preferences.get("make"))
            if maybe_model:
                preferences["model"] = maybe_model
                if not preferences.get("make"):
                    derived_make = self.catalog_service.find_make_by_model(maybe_model)
                    if derived_make:
                        preferences["make"] = derived_make

        if "max_km" not in preferences:
            km = self._extract_kilometers(request.message)
            if km:
                preferences["max_km"] = km

        if "min_year" not in preferences:
            year = self._extract_year(request.message)
            if year:
                preferences["min_year"] = year

        if "max_price" not in preferences:
            price = self._extract_price_hint(request.message)
            if price:
                preferences["max_price"] = price

        data["preferences"] = preferences or None

        if not data.get("financing"):
            financing = self._extract_financing(request.message)
            if financing:
                data["financing"] = financing.model_dump()

        return ChatRequest(**data)

    def detect_intent(self, message: str) -> str:
        # Deprecated: intent classification now handled by IntentClassifier
        _ = message
        return "ambiguous"

    def identify_missing_fields(
        self, original: ChatRequest, enriched: ChatRequest
    ) -> list[str]:
        """Highlight key fields still missing after parsing."""
        missing: list[str] = []
        prefs = enriched.preferences or {}

        if not prefs.get("make"):
            missing.append("marca")
        if not prefs.get("model"):
            missing.append("modelo")
        if not prefs.get("max_km"):
            missing.append("kilometraje objetivo")
        if not prefs.get("max_price"):
            missing.append("presupuesto")
        if not prefs.get("min_year"):
            missing.append("año mínimo")

        if original.financing is None:
            financing = enriched.financing
            if not financing:
                missing.append("datos de financiamiento (precio y plazos)")
            else:
                if financing.down_payment is None or financing.down_payment == 0:
                    missing.append("enganche aproximado")
                if not financing.years:
                    missing.append("plazo en años")

        return missing

    def _extract_make(self, message: str) -> str | None:
        text = message.lower()
        for make in self.catalog_service.list_makes():
            if make.lower() in text:
                return make
        for alias, canonical in ALIAS_BRANDS.items():
            if alias in text:
                return canonical
        return None

    def _extract_model(self, message: str, make: str | None) -> str | None:
        candidates = (
            self.catalog_service.list_models(make) if make else self.catalog_service.list_models()
        )
        text = message.lower()
        for model in candidates:
            model_clean = model.lower()
            if len(model_clean) < 3:
                continue
            if model_clean in text:
                return model
        for alias, canonical in ALIAS_MODELS.items():
            if alias in text:
                return canonical
        return None

    @staticmethod
    def _extract_kilometers(message: str) -> int | None:
        match = KM_PATTERN.search(message)
        if not match:
            return None
        groups = match.groups()
        number = 0
        if groups[1]:
            number = int(f"{groups[0]}{groups[1]}")
        else:
            number = int(groups[0])
            if groups[2]:
                number *= 1000
        return number

    @staticmethod
    def _extract_year(message: str) -> int | None:
        years = [int(value) for value in YEAR_PATTERN.findall(message)
                 if 2000 <= int(value) <= 2030]
        if not years:
            return None
        return min(years)

    @staticmethod
    def _parse_amount(token: str, multiplier: str | None) -> float:
        normalized = token.replace(",", "").replace(".", "")
        value = float(normalized)
        if multiplier:
            multiplier = multiplier.lower()
            if multiplier in {"k", "mil"}:
                value *= 1000
        return value

    def _extract_price_hint(self, message: str) -> float | None:
        for match in AMOUNT_PATTERN.finditer(message):
            token, multiplier = match.groups()
            amount = self._parse_amount(token, multiplier)
            if 1900 <= amount <= 2100:
                continue  # probable year
            if amount > 50000:  # assume MXN
                return amount
        return None

    def _extract_financing(self, message: str) -> FinancingInput | None:
        amounts = []
        for match in AMOUNT_PATTERN.finditer(message):
            token, multiplier = match.groups()
            amount = self._parse_amount(token, multiplier)
            if 1900 <= amount <= 2100:
                continue
            if amount > 10000:
                amounts.append(amount)

        if not amounts:
            return None

        years_match = YEARS_TERM_PATTERN.search(message)
        years = int(years_match.group(1)) if years_match else None
        enganche_match = ENGANCHE_PATTERN.search(message)

        price = amounts[0]
        down_payment = None

        if len(amounts) > 1:
            down_payment = amounts[1]
        elif enganche_match and len(amounts) == 1:
            down_payment = amounts[0]

        if price and down_payment and price <= down_payment:
            price, down_payment = down_payment, price

        if not years:
            return None
        if not price:
            return None

        down_payment = down_payment or 0
        return FinancingInput(car_price=price, down_payment=down_payment, years=years)
