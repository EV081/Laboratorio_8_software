from decimal import Decimal

from rewards_service.domain.model.reward_account import RewardAccount
from rewards_service.infrastructure.persistence.in_memory_repo import (
    InMemoryRewardRepository,
)


def test_find_returns_none_for_unknown_card():
    repo = InMemoryRewardRepository()
    assert repo.find_by_card("missing") is None


def test_save_then_find_returns_same_account():
    repo = InMemoryRewardRepository()
    account = RewardAccount("C1", points=Decimal("25"))
    repo.save(account)
    found = repo.find_by_card("C1")
    assert found is account
    assert found.points == Decimal("25")


def test_save_overwrites_previous_account():
    repo = InMemoryRewardRepository()
    repo.save(RewardAccount("C1", points=Decimal("5")))
    repo.save(RewardAccount("C1", points=Decimal("50")))
    assert repo.find_by_card("C1").points == Decimal("50")
