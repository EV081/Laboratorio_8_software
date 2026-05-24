import json
from decimal import Decimal
from unittest.mock import MagicMock

from rewards_service.infrastructure.messaging.rabbit_notification_publisher import (
    RabbitNotificationPublisher,
)


def test_publishes_payload_to_queue():
    fake_channel = MagicMock()
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel

    publisher = RabbitNotificationPublisher(
        connection_factory=lambda: fake_connection,
        queue="reward.processed",
    )

    publisher.publish_reward_processed("C1", Decimal("10.00"), Decimal("50.00"))

    fake_channel.queue_declare.assert_called_once_with(
        queue="reward.processed", durable=True
    )
    _, kwargs = fake_channel.basic_publish.call_args
    body = json.loads(kwargs["body"].decode("utf-8"))
    assert body == {
        "card_number": "C1",
        "points_added": "10.00",
        "total_points": "50.00",
    }
    fake_connection.close.assert_called_once()


def test_connection_is_closed_on_error():
    fake_channel = MagicMock()
    fake_channel.basic_publish.side_effect = RuntimeError("boom")
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel

    publisher = RabbitNotificationPublisher(lambda: fake_connection, queue="q")

    try:
        publisher.publish_reward_processed("C1", Decimal("1"), Decimal("1"))
    except RuntimeError:
        pass

    fake_connection.close.assert_called_once()
