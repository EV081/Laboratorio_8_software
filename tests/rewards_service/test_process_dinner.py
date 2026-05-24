from datetime import datetime
from decimal import Decimal
from typing import List, Tuple

from rewards_service.application.process_dinner import ProcessDinnerUseCase
from rewards_service.domain.model.dinner_event import DinnerEvent
from rewards_service.domain.policy.points_policy import PercentagePointsPolicy
from rewards_service.domain.ports.notification_publisher import NotificationPublisher
from rewards_service.infrastructure.persistence.in_memory_repo import (
    InMemoryRewardRepository,
)


class _RecordingNotifier(NotificationPublisher):
    def __init__(self) -> None:
        self.events: List[Tuple[str, Decimal, Decimal]] = []

    def publish_reward_processed(
        self, card_number: str, points_added: Decimal, total_points: Decimal
    ) -> None:
        self.events.append((card_number, points_added, total_points))


def _make_event(card: str = "C1", amount: str = "100") -> DinnerEvent:
    return DinnerEvent(
        amount=Decimal(amount),
        card_number=card,
        restaurant_code="R1",
        occurred_at=datetime(2026, 1, 1, 10, 0),
    )


def test_process_dinner_creates_account_when_missing():
    repo = InMemoryRewardRepository()
    notifier = _RecordingNotifier()
    use_case = ProcessDinnerUseCase(repo, PercentagePointsPolicy(), notifier)

    account = use_case.execute(_make_event())

    assert account.card_number == "C1"
    assert account.points == Decimal("10.00")
    assert repo.find_by_card("C1") is account


def test_process_dinner_accumulates_on_existing_account():
    repo = InMemoryRewardRepository()
    notifier = _RecordingNotifier()
    use_case = ProcessDinnerUseCase(repo, PercentagePointsPolicy(), notifier)

    use_case.execute(_make_event(amount="100"))
    use_case.execute(_make_event(amount="50"))

    assert repo.find_by_card("C1").points == Decimal("15.00")


def test_process_dinner_publishes_notification():
    repo = InMemoryRewardRepository()
    notifier = _RecordingNotifier()
    use_case = ProcessDinnerUseCase(repo, PercentagePointsPolicy(), notifier)

    use_case.execute(_make_event(amount="200"))

    assert notifier.events == [("C1", Decimal("20.00"), Decimal("20.00"))]
