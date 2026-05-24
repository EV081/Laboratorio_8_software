import json
from decimal import Decimal
from typing import Callable

import pika

from rewards_service.domain.ports.notification_publisher import NotificationPublisher


class RabbitNotificationPublisher(NotificationPublisher):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        exchange: str = "",
    ) -> None:
        self._connection_factory = connection_factory
        self._queue = queue
        self._exchange = exchange

    def publish_reward_processed(
        self, card_number: str, points_added: Decimal, total_points: Decimal
    ) -> None:
        payload = json.dumps(
            {
                "card_number": card_number,
                "points_added": str(points_added),
                "total_points": str(total_points),
            }
        )
        connection = self._connection_factory()
        try:
            channel = connection.channel()
            channel.queue_declare(queue=self._queue, durable=True)
            channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._queue,
                body=payload.encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
            )
        finally:
            connection.close()
