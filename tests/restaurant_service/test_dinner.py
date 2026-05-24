from datetime import datetime
from decimal import Decimal

import pytest

from restaurant_service.domain.model.dinner import Dinner


def _now() -> datetime:
    return datetime(2026, 5, 24, 12, 30, 0)


def test_dinner_is_created_with_valid_fields():
    dinner = Dinner(Decimal("100.50"), "1234567890123456", "REST001", _now())
    assert dinner.amount == Decimal("100.50")
    assert dinner.card_number == "1234567890123456"
    assert dinner.restaurant_code == "REST001"
    assert dinner.occurred_at == _now()


def test_dinner_is_immutable():
    dinner = Dinner(Decimal("10"), "C1", "R1", _now())
    with pytest.raises(Exception):
        dinner.amount = Decimal("20")  # type: ignore[misc]


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-5")])
def test_dinner_rejects_non_positive_amount(amount):
    with pytest.raises(ValueError, match="amount"):
        Dinner(amount, "C1", "R1", _now())


@pytest.mark.parametrize("card", ["", "   "])
def test_dinner_rejects_empty_card_number(card):
    with pytest.raises(ValueError, match="card_number"):
        Dinner(Decimal("10"), card, "R1", _now())


@pytest.mark.parametrize("code", ["", "   "])
def test_dinner_rejects_empty_restaurant_code(code):
    with pytest.raises(ValueError, match="restaurant_code"):
        Dinner(Decimal("10"), "C1", code, _now())


def test_dinner_rejects_invalid_occurred_at():
    with pytest.raises(ValueError, match="occurred_at"):
        Dinner(Decimal("10"), "C1", "R1", "not-a-datetime")  # type: ignore[arg-type]
