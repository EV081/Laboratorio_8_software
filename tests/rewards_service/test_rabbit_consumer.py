import json
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from rewards_service.application.process_dinner import ProcessDinnerUseCase
from rewards_service.domain.policy.points_policy import PercentagePointsPolicy
from rewards_service.domain.ports.notification_publisher import NotificationPublisher
from rewards_service.infrastructure.messaging.rabbit_consumer import (
    RabbitDinnerConsumer,
)
from rewards_service.infrastructure.persistence.in_memory_repo import (
    InMemoryRewardRepository,
)


class _NullNotifier(NotificationPublisher):
    def publish_reward_processed(self, card_number, points_added, total_points):
        pass


def _build_consumer() -> tuple[RabbitDinnerConsumer, InMemoryRewardRepository, MagicMock]:
    repo = InMemoryRewardRepository()
    use_case = ProcessDinnerUseCase(repo, PercentagePointsPolicy(), _NullNotifier())
    fake_channel = MagicMock()
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel
    consumer = RabbitDinnerConsumer(
        connection_factory=lambda: fake_connection,
        queue="dinner.registered",
        use_case=use_case,
    )
    return consumer, repo, fake_channel


def test_on_message_processes_valid_event():
    consumer, repo, _ = _build_consumer()
    body = json.dumps(
        {
            "amount": "100",
            "card_number": "C1",
            "restaurant_code": "R1",
            "occurred_at": datetime(2026, 1, 1, 10, 0).isoformat(),
        }
    ).encode("utf-8")

    consumer.on_message(None, None, None, body)

    assert repo.find_by_card("C1").points == Decimal("10.00")


def test_start_registers_consumer_and_starts_consuming():
    consumer, _, fake_channel = _build_consumer()
    consumer.start()
    fake_channel.queue_declare.assert_called_once_with(
        queue="dinner.registered", durable=True
    )
    fake_channel.basic_consume.assert_called_once()
    fake_channel.start_consuming.assert_called_once()
