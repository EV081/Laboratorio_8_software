from decimal import Decimal

import pytest

from rewards_service.domain.model.reward_account import RewardAccount


def test_account_starts_with_zero_points():
    account = RewardAccount("C1")
    assert account.points == Decimal("0")


def test_account_accumulates_points():
    account = RewardAccount("C1")
    account.add_points(Decimal("10"))
    account.add_points(Decimal("5.50"))
    assert account.points == Decimal("15.50")


def test_account_rejects_empty_card_number():
    with pytest.raises(ValueError):
        RewardAccount("")


def test_account_rejects_negative_initial_points():
    with pytest.raises(ValueError):
        RewardAccount("C1", points=Decimal("-1"))


def test_add_points_rejects_negative_amount():
    account = RewardAccount("C1")
    with pytest.raises(ValueError):
        account.add_points(Decimal("-1"))
