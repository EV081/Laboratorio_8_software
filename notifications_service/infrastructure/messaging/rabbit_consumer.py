import json
from decimal import Decimal
from typing import Callable

import pika

from notifications_service.application.send_notification import (
    SendNotificationUseCase,
)
from notifications_service.domain.model.notification import Notification
from shared.messaging.rabbit_base import BaseRabbitConsumer


class RabbitNotificationConsumer(BaseRabbitConsumer[Notification]):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        use_case: SendNotificationUseCase,
    ) -> None:
        super().__init__(connection_factory, queue)
        self._use_case = use_case

    def _deserialize(self, body: bytes) -> Notification:
        data = json.loads(body.decode("utf-8"))
        return Notification(
            card_number=data["card_number"],
            points_added=Decimal(str(data["points_added"])),
            total_points=Decimal(str(data["total_points"])),
        )

    def _handle(self, message: Notification) -> None:
        self._use_case.execute(message)
