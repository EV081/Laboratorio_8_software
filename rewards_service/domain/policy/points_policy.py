from abc import ABC, abstractmethod
from decimal import Decimal


class PointsPolicy(ABC):
    @abstractmethod
    def calculate(self, amount: Decimal) -> Decimal:
        raise NotImplementedError


class PercentagePointsPolicy(PointsPolicy):
    def __init__(self, percentage: Decimal = Decimal("0.10")) -> None:
        if percentage <= 0:
            raise ValueError("percentage must be positive")
        self._percentage = percentage

    def calculate(self, amount: Decimal) -> Decimal:
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return (amount * self._percentage).quantize(Decimal("0.01"))
