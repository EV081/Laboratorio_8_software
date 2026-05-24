import json
from typing import Callable

import pika

from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.domain.ports.dinner_publisher import DinnerPublisher


class RabbitDinnerPublisher(DinnerPublisher):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        exchange: str = "",
    ) -> None:
        self._connection_factory = connection_factory
        self._queue = queue
        self._exchange = exchange

    def publish(self, dinner: Dinner) -> None:
        payload = self._serialize(dinner)
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

    @staticmethod
    def _serialize(dinner: Dinner) -> str:
        return json.dumps(
            {
                "amount": str(dinner.amount),
                "card_number": dinner.card_number,
                "restaurant_code": dinner.restaurant_code,
                "occurred_at": dinner.occurred_at.isoformat(),
            }
        )
