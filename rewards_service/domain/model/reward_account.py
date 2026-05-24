from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class RewardAccount:
    card_number: str
    points: Decimal = field(default_factory=lambda: Decimal("0"))

    def __post_init__(self) -> None:
        if not self.card_number or not self.card_number.strip():
            raise ValueError("card_number cannot be empty")
        if self.points < 0:
            raise ValueError("points cannot be negative")

    def add_points(self, amount: Decimal) -> None:
        if amount < 0:
            raise ValueError("cannot add negative points")
        self.points += amount
