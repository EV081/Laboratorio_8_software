import json
from decimal import Decimal
from typing import Callable

import pika

from notifications_service.application.send_notification import (
    SendNotificationUseCase,
)
from notifications_service.domain.model.notification import Notification


class RabbitNotificationConsumer:
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        use_case: SendNotificationUseCase,
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
        notification = self._deserialize(body)
        self._use_case.execute(notification)

    @staticmethod
    def _deserialize(body: bytes) -> Notification:
        data = json.loads(body.decode("utf-8"))
        return Notification(
            card_number=data["card_number"],
            points_added=Decimal(str(data["points_added"])),
            total_points=Decimal(str(data["total_points"])),
        )
