"""Service responsible for loading and querying the car catalog."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from app.domain.models import Car


class CatalogService:
    """Handle catalog data sourced from a CSV file."""

    def __init__(self) -> None:
        self._catalog: list[Car] = []

    def load_catalog(self, path: str) -> None:
        """Load catalog data from the provided CSV path."""
        csv_path = Path(path)
        if not csv_path.exists():
            msg = f"Catalog CSV not found at {path}"
            raise FileNotFoundError(msg)

        with csv_path.open(encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            self._catalog = [self._row_to_car(row) for row in reader]

    def search_cars(self, preferences: dict | None = None) -> list[Car]:
        """Return cars that match user preferences."""
        if not self._catalog:
            return []

        filters = preferences or {}
        results: list[Car] = []
        for car in self._catalog:
            if self._matches_preferences(car, filters):
                results.append(car)
        return results

    @staticmethod
    def _row_to_car(row: dict[str, Any]) -> Car:
        """Convert CSV row into a Car model."""
        return Car(
            stock_id=row.get("stock_id", ""),
            km=CatalogService._to_int(row.get("km")),
            price=CatalogService._to_float(row.get("price")),
            make=row.get("make", ""),
            model=row.get("model", ""),
            year=CatalogService._to_int(row.get("year")),
            version=row.get("version", ""),
            bluetooth=CatalogService._to_bool(row.get("bluetooth")),
            length_mm=CatalogService._to_float(row.get("largo")),
            width_mm=CatalogService._to_float(row.get("ancho")),
            height_mm=CatalogService._to_float(row.get("altura")),
            car_play=CatalogService._to_bool(row.get("car_play")),
        )

    @staticmethod
    def _to_int(value: Any) -> int:
        return int(float(value)) if value not in (None, "", "None") else 0

    @staticmethod
    def _to_float(value: Any) -> float:
        return float(value) if value not in (None, "", "None") else 0.0

    @staticmethod
    def _to_bool(value: Any) -> bool | None:
        normalized = str(value or "").strip().lower()
        if not normalized:
            return None
        return normalized in {"sí", "si", "true", "1"}

    @staticmethod
    def _matches_preferences(car: Car, preferences: dict[str, Any]) -> bool:
        """Evaluate whether a car satisfies the basic preference filters."""
        make = preferences.get("make")
        if make and make.lower() not in car.make.lower():
            return False

        model = preferences.get("model")
        if model and model.lower() not in car.model.lower():
            return False

        max_price = preferences.get("max_price")
        if max_price is not None and car.price > float(max_price):
            return False

        max_km = preferences.get("max_km")
        if max_km is not None and car.km > int(max_km):
            return False

        min_year = preferences.get("min_year")
        if min_year is not None and car.year < int(min_year):
            return False

        return True
