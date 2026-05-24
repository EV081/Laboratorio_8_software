import json
from datetime import datetime
from decimal import Decimal
from typing import Callable

import pika

from rewards_service.application.process_dinner import ProcessDinnerUseCase
from rewards_service.domain.model.dinner_event import DinnerEvent
from shared.messaging.rabbit_base import BaseRabbitConsumer


class RabbitDinnerConsumer(BaseRabbitConsumer[DinnerEvent]):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        use_case: ProcessDinnerUseCase,
    ) -> None:
        super().__init__(connection_factory, queue)
        self._use_case = use_case

    def _deserialize(self, body: bytes) -> DinnerEvent:
        data = json.loads(body.decode("utf-8"))
        return DinnerEvent(
            amount=Decimal(str(data["amount"])),
            card_number=data["card_number"],
            restaurant_code=data["restaurant_code"],
            occurred_at=datetime.fromisoformat(data["occurred_at"]),
        )

    def _handle(self, message: DinnerEvent) -> None:
        self._use_case.execute(message)
