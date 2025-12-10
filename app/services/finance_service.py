"""Utility functions for financing calculations."""

from __future__ import annotations

from app.domain.models import FinancingPlan

MIN_YEARS = 3
MAX_YEARS = 6


def calculate_financing(
    price: float,
    down_payment: float,
    years: int,
    interest_rate: float = 0.10,
) -> FinancingPlan:
    """Calculate a financing plan for a vehicle purchase."""
    _validate_inputs(price, down_payment, years, interest_rate)

    principal = price - down_payment
    months = years * 12
    monthly_rate = interest_rate / 12

    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / (
            (1 + monthly_rate) ** months - 1
        )

    total_paid = monthly_payment * months + down_payment

    return FinancingPlan(
        months=months,
        monthly_payment=round(monthly_payment, 2),
        total_paid=round(total_paid, 2),
        interest_rate=interest_rate,
    )


def _validate_inputs(price: float, down_payment: float, years: int, interest_rate: float) -> None:
    if price <= 0:
        raise ValueError("Price must be greater than zero.")
    if down_payment < 0 or down_payment >= price:
        raise ValueError("Down payment must be between 0 and price.")
    if years < MIN_YEARS or years > MAX_YEARS:
        raise ValueError(f"Years must be between {MIN_YEARS} and {MAX_YEARS}.")
    if interest_rate < 0:
        raise ValueError("Interest rate must be non-negative.")
