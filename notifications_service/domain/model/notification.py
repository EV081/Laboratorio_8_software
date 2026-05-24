from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Notification:
    card_number: str
    points_added: Decimal
    total_points: Decimal

    def __post_init__(self) -> None:
        if not self.card_number or not self.card_number.strip():
            raise ValueError("card_number cannot be empty")
        if self.points_added < 0:
            raise ValueError("points_added cannot be negative")
        if self.total_points < 0:
            raise ValueError("total_points cannot be negative")

    def masked_card(self) -> str:
        if len(self.card_number) <= 4:
            return self.card_number
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]

    def message(self) -> str:
        return (
            f"Hola cliente {self.masked_card()}: se acreditaron "
            f"{self.points_added} puntos. Total acumulado: {self.total_points}."
        )
