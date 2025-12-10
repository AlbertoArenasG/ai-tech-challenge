"""Request/response schemas for public API endpoints."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.domain.models import FinancingPlan, Recommendation


class FinancingInput(BaseModel):
    """Payload describing the financing needs of a customer conversation."""

    car_price: float = Field(gt=0)
    down_payment: float = Field(ge=0)
    years: int = Field(ge=1)


class ChatRequest(BaseModel):
    """Envelope for the `/chat` endpoint."""

    user_id: str
    message: str
    channel: str | None = None
    preferences: dict[str, Any] | None = None
    financing: FinancingInput | None = None


class ChatResponse(BaseModel):
    """LLM response enriched with structured recommendations."""

    message: str
    recommendations: list[Recommendation] = Field(default_factory=list)
    financing_plan: FinancingPlan | None = None
