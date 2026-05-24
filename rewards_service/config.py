import os
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class RewardsConfig:
    host: str
    port: int
    virtual_host: str
    user: str
    password: str
    dinner_queue: str
    notification_queue: str
    points_percentage: Decimal


def load_config() -> RewardsConfig:
    return RewardsConfig(
        host=os.getenv("RABBIT_HOST", "213.199.42.57"),
        port=int(os.getenv("RABBIT_PORT", "5672")),
        virtual_host=os.getenv("RABBIT_VHOST", "/"),
        user=os.getenv("RABBIT_USER", "students"),
        password=os.getenv("RABBIT_PASSWORD", "Ut3c2026"),
        dinner_queue=os.getenv("DINNER_QUEUE", "dinner.registered"),
        notification_queue=os.getenv("NOTIFICATION_QUEUE", "reward.processed"),
        points_percentage=Decimal(os.getenv("POINTS_PERCENTAGE", "0.10")),
    )
