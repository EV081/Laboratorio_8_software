from abc import ABC, abstractmethod

from restaurant_service.domain.model.dinner import Dinner


class DinnerPublisher(ABC):
    @abstractmethod
    def publish(self, dinner: Dinner) -> None:
        raise NotImplementedError
