import json

from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.domain.ports.dinner_publisher import DinnerPublisher
from shared.messaging.rabbit_base import BaseRabbitPublisher


class RabbitDinnerPublisher(BaseRabbitPublisher[Dinner], DinnerPublisher):
    def _serialize(self, message: Dinner) -> str:
        return json.dumps(
            {
                "amount": str(message.amount),
                "card_number": message.card_number,
                "restaurant_code": message.restaurant_code,
                "occurred_at": message.occurred_at.isoformat(),
            }
        )
