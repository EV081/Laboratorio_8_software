from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.domain.ports.dinner_publisher import DinnerPublisher


class RegisterDinnerUseCase:
    def __init__(self, publisher: DinnerPublisher) -> None:
        self._publisher = publisher

    def execute(self, dinner: Dinner) -> None:
        self._publisher.publish(dinner)
