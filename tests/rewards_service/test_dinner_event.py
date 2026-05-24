from datetime import datetime
from decimal import Decimal

import pytest

from rewards_service.domain.model.dinner_event import DinnerEvent


def test_dinner_event_is_created_with_valid_fields():
    event = DinnerEvent(Decimal("10"), "C1", "R1", datetime(2026, 1, 1))
    assert event.amount == Decimal("10")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-1")])
def test_dinner_event_rejects_non_positive_amount(amount):
    with pytest.raises(ValueError):
        DinnerEvent(amount, "C1", "R1", datetime(2026, 1, 1))


def test_dinner_event_rejects_empty_card():
    with pytest.raises(ValueError):
        DinnerEvent(Decimal("1"), "", "R1", datetime(2026, 1, 1))


def test_dinner_event_rejects_empty_restaurant():
    with pytest.raises(ValueError):
        DinnerEvent(Decimal("1"), "C1", "", datetime(2026, 1, 1))


def test_dinner_event_rejects_invalid_datetime():
    with pytest.raises(ValueError):
        DinnerEvent(Decimal("1"), "C1", "R1", "now")  # type: ignore[arg-type]
