import json
from dataclasses import dataclass
from decimal import Decimal

from rewards_service.domain.ports.notification_publisher import NotificationPublisher
from shared.messaging.rabbit_base import BaseRabbitPublisher


@dataclass(frozen=True)
class _RewardProcessedMessage:
    card_number: str
    points_added: Decimal
    total_points: Decimal


class _RewardProcessedRabbitPublisher(BaseRabbitPublisher[_RewardProcessedMessage]):
    def _serialize(self, message: _RewardProcessedMessage) -> str:
        return json.dumps(
            {
                "card_number": message.card_number,
                "points_added": str(message.points_added),
                "total_points": str(message.total_points),
            }
        )


class RabbitNotificationPublisher(NotificationPublisher):
    def __init__(self, connection_factory, queue: str, exchange: str = "") -> None:
        self._inner = _RewardProcessedRabbitPublisher(
            connection_factory, queue, exchange
        )

    def publish_reward_processed(
        self, card_number: str, points_added: Decimal, total_points: Decimal
    ) -> None:
        self._inner.publish(
            _RewardProcessedMessage(card_number, points_added, total_points)
        )
