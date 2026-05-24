from datetime import datetime
from decimal import Decimal

from restaurant_service.application.register_dinner import RegisterDinnerUseCase
from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.domain.ports.dinner_publisher import DinnerPublisher


class _FakePublisher(DinnerPublisher):
    def __init__(self) -> None:
        self.published: list[Dinner] = []

    def publish(self, dinner: Dinner) -> None:
        self.published.append(dinner)


def test_use_case_publishes_dinner_through_port():
    publisher = _FakePublisher()
    use_case = RegisterDinnerUseCase(publisher)
    dinner = Dinner(Decimal("50"), "C1", "R1", datetime(2026, 1, 1, 10, 0))

    use_case.execute(dinner)

    assert publisher.published == [dinner]


def test_use_case_handles_multiple_dinners():
    publisher = _FakePublisher()
    use_case = RegisterDinnerUseCase(publisher)
    for amount in [Decimal("10"), Decimal("20"), Decimal("30")]:
        use_case.execute(Dinner(amount, "C1", "R1", datetime(2026, 1, 1, 10, 0)))
    assert len(publisher.published) == 3
