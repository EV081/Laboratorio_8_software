from abc import ABC, abstractmethod
from decimal import Decimal


class NotificationPublisher(ABC):
    @abstractmethod
    def publish_reward_processed(
        self, card_number: str, points_added: Decimal, total_points: Decimal
    ) -> None:
        raise NotImplementedError
