from decimal import Decimal

import pytest

from rewards_service.domain.policy.points_policy import PercentagePointsPolicy


def test_default_policy_gives_10_percent():
    policy = PercentagePointsPolicy()
    assert policy.calculate(Decimal("100")) == Decimal("10.00")


def test_custom_percentage_is_applied():
    policy = PercentagePointsPolicy(Decimal("0.05"))
    assert policy.calculate(Decimal("200")) == Decimal("10.00")


def test_policy_rounds_to_two_decimals():
    policy = PercentagePointsPolicy(Decimal("0.10"))
    assert policy.calculate(Decimal("33.33")) == Decimal("3.33")


def test_policy_rejects_negative_amount():
    policy = PercentagePointsPolicy()
    with pytest.raises(ValueError):
        policy.calculate(Decimal("-1"))


def test_policy_rejects_non_positive_percentage():
    with pytest.raises(ValueError):
        PercentagePointsPolicy(Decimal("0"))
