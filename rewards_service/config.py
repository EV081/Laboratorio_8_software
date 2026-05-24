import os
from dataclasses import dataclass
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()


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


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def load_config() -> RewardsConfig:
    return RewardsConfig(
        host=_require("RABBIT_HOST"),
        port=int(_require("RABBIT_PORT")),
        virtual_host=_require("RABBIT_VHOST"),
        user=_require("RABBIT_USER"),
        password=_require("RABBIT_PASSWORD"),
        dinner_queue=os.getenv("DINNER_QUEUE", "dinner.registered"),
        notification_queue=os.getenv("NOTIFICATION_QUEUE", "reward.processed"),
        points_percentage=Decimal(os.getenv("POINTS_PERCENTAGE", "0.10")),
    )
