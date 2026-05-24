import json
from datetime import datetime
from decimal import Decimal
from typing import Callable

import pika

from rewards_service.application.process_dinner import ProcessDinnerUseCase
from rewards_service.domain.model.dinner_event import DinnerEvent


class RabbitDinnerConsumer:
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        use_case: ProcessDinnerUseCase,
    ) -> None:
        self._connection_factory = connection_factory
        self._queue = queue
        self._use_case = use_case

    def start(self) -> None:
        connection = self._connection_factory()
        channel = connection.channel()
        channel.queue_declare(queue=self._queue, durable=True)
        channel.basic_consume(
            queue=self._queue,
            on_message_callback=self.on_message,
            auto_ack=True,
        )
        channel.start_consuming()

    def on_message(self, _channel, _method, _properties, body: bytes) -> None:
        event = self._deserialize(body)
        self._use_case.execute(event)

    @staticmethod
    def _deserialize(body: bytes) -> DinnerEvent:
        data = json.loads(body.decode("utf-8"))
        return DinnerEvent(
            amount=Decimal(str(data["amount"])),
            card_number=data["card_number"],
            restaurant_code=data["restaurant_code"],
            occurred_at=datetime.fromisoformat(data["occurred_at"]),
        )
