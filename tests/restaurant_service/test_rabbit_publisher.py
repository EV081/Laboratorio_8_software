import json
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.infrastructure.messaging.rabbit_publisher import (
    RabbitDinnerPublisher,
)


def test_publisher_serializes_dinner_and_calls_basic_publish():
    fake_channel = MagicMock()
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel

    publisher = RabbitDinnerPublisher(
        connection_factory=lambda: fake_connection,
        queue="dinner.registered",
    )
    dinner = Dinner(
        Decimal("99.99"),
        "4111111111111111",
        "REST-1",
        datetime(2026, 5, 24, 19, 30, 0),
    )

    publisher.publish(dinner)

    fake_channel.queue_declare.assert_called_once_with(
        queue="dinner.registered", durable=True
    )
    args, kwargs = fake_channel.basic_publish.call_args
    assert kwargs["routing_key"] == "dinner.registered"
    body = json.loads(kwargs["body"].decode("utf-8"))
    assert body["amount"] == "99.99"
    assert body["card_number"] == "4111111111111111"
    assert body["restaurant_code"] == "REST-1"
    assert body["occurred_at"] == "2026-05-24T19:30:00"
    fake_connection.close.assert_called_once()


def test_publisher_closes_connection_even_on_failure():
    fake_channel = MagicMock()
    fake_channel.basic_publish.side_effect = RuntimeError("boom")
    fake_connection = MagicMock()
    fake_connection.channel.return_value = fake_channel

    publisher = RabbitDinnerPublisher(lambda: fake_connection, queue="q")
    dinner = Dinner(Decimal("1"), "C1", "R1", datetime(2026, 1, 1))

    try:
        publisher.publish(dinner)
    except RuntimeError:
        pass

    fake_connection.close.assert_called_once()
