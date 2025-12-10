"""Adapter utilities for integrating with Twilio WhatsApp."""
from __future__ import annotations

from typing import Any

from app.domain.schemas import ChatRequest, ChatResponse

MAX_WHATSAPP_LENGTH = 1500


def parse_twilio_payload(payload: dict[str, Any]) -> ChatRequest:
    """Convert Twilio webhook payload into ChatRequest."""
    user_id = payload.get("WaId") or payload.get("From", "").replace("whatsapp:", "")
    text = payload.get("Body", "").strip()

    return ChatRequest(
        user_id=user_id or "unknown",
        message=text or "",
        channel="whatsapp",
    )


def format_twilio_response(response: ChatResponse) -> str:
    """Render a chat response as plain text for Twilio."""
    lines = [response.message]
    if response.recommendations:
        recommendation_lines = [
            f"- {rec.car.make} {rec.car.model} {rec.car.year} | ${rec.car.price:,.0f}"
            for rec in response.recommendations
        ]
        lines.append("Recomendaciones:\n" + "\n".join(recommendation_lines))

    if response.financing_plan:
        plan = response.financing_plan
        lines.append(
            f"Financiamiento: {plan.months} meses, pago mensual ${plan.monthly_payment}, total ${plan.total_paid}."
        )

    response_text = "\n\n".join(lines)
    return _truncate(response_text)


def _truncate(text: str) -> str:
    if len(text) <= MAX_WHATSAPP_LENGTH:
        return text
    return text[: MAX_WHATSAPP_LENGTH - 3].rstrip() + "..."
