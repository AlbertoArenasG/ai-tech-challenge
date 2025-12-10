"""Domain models for the Kavak commercial bot."""
from __future__ import annotations

from pydantic import BaseModel


class Car(BaseModel):
    """Representation of a car in the Kavak catalog."""

    stock_id: str
    km: int
    price: float
    make: str
    model: str
    year: int
    version: str
    bluetooth: bool | None = None
    length_mm: float | None = None
    width_mm: float | None = None
    height_mm: float | None = None
    car_play: bool | None = None
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
