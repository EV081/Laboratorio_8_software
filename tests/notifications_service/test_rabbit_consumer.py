import json
from decimal import Decimal
from typing import List
from unittest.mock import MagicMock

from notifications_service.application.send_notification import (
    SendNotificationUseCase,
)
from notifications_service.domain.model.notification import Notification
from notifications_service.domain.ports.notification_sender import NotificationSender
from notifications_service.infrastructure.messaging.rabbit_consumer import (
    RabbitNotificationConsumer,
)


class _CapturingSender(NotificationSender):
    def __init__(self) -> None:
        self.sent: List[Notification] = []

    def send(self, notification: Notification) -> None:
        self.sent.append(notification)


def _build_consumer():
    sender = _CapturingSender()
    use_case = SendNotificationUseCase(sender)
    fake_channel = MagicMock()
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel
    consumer = RabbitNotificationConsumer(
        connection_factory=lambda: fake_connection,
        queue="reward.processed",
        use_case=use_case,
    )
    return consumer, sender, fake_channel


def test_on_message_deserializes_and_sends():
    consumer, sender, _ = _build_consumer()
    body = json.dumps(
        {
            "card_number": "C1",
            "points_added": "10.00",
            "total_points": "50.00",
        }
    ).encode("utf-8")

    consumer.on_message(None, None, None, body)

    assert len(sender.sent) == 1
    assert sender.sent[0].card_number == "C1"
    assert sender.sent[0].points_added == Decimal("10.00")


def test_start_wires_consumption():
    consumer, _, fake_channel = _build_consumer()
    consumer.start()
    fake_channel.queue_declare.assert_called_once_with(
        queue="reward.processed", durable=True
    )
    fake_channel.start_consuming.assert_called_once()
