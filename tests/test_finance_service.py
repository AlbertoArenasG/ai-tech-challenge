"""Tests for financing calculations."""
import pytest

from app.services.finance_service import calculate_financing


def test_calculate_financing_returns_expected_plan() -> None:
    plan = calculate_financing(price=300000, down_payment=60000, years=4, interest_rate=0.10)

    assert plan.months == 48
    assert plan.monthly_payment > 0
    assert plan.total_paid > 300000  # interest should increase total cost
    assert plan.interest_rate == 0.10


def test_calculate_financing_validates_input_ranges() -> None:
    with pytest.raises(ValueError):
        calculate_financing(price=0, down_payment=1000, years=4)

    with pytest.raises(ValueError):
        calculate_financing(price=100000, down_payment=120000, years=4)

    with pytest.raises(ValueError):
        calculate_financing(price=100000, down_payment=10000, years=2)
