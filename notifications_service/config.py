import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class NotificationsConfig:
    host: str
    port: int
    virtual_host: str
    user: str
    password: str
    queue: str


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def load_config() -> NotificationsConfig:
    return NotificationsConfig(
        host=_require("RABBIT_HOST"),
        port=int(_require("RABBIT_PORT")),
        virtual_host=_require("RABBIT_VHOST"),
        user=_require("RABBIT_USER"),
        password=_require("RABBIT_PASSWORD"),
        queue=os.getenv("NOTIFICATION_QUEUE", "reward.processed"),
    )
