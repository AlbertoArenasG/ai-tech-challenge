"""Domain models for the Kavak commercial bot."""
from __future__ import annotations

from pydantic import BaseModel


class Car(BaseModel):
    """Representation of a car in the Kavak catalog."""

    id: str
    brand: str
    model: str
    year: int
    price: float
    kilometers: int
    # TODO: Revisit attributes once the final CSV schema (trim, transmission, location) is confirmed.


class Recommendation(BaseModel):
    """Pair a recommended car with the reasoning behind it."""

    car: Car
    reason: str


class FinancingPlan(BaseModel):
    """Simple financing projection for a vehicle purchase."""

    months: int
    monthly_payment: float
    total_paid: float
    interest_rate: float
