from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Dinner:
    amount: Decimal
    card_number: str
    restaurant_code: str
    occurred_at: datetime

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if not self.card_number or not self.card_number.strip():
            raise ValueError("card_number cannot be empty")
        if not self.restaurant_code or not self.restaurant_code.strip():
            raise ValueError("restaurant_code cannot be empty")
        if not isinstance(self.occurred_at, datetime):
            raise ValueError("occurred_at must be a datetime")
