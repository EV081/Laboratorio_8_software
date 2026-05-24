import os
from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationsConfig:
    host: str
    port: int
    virtual_host: str
    user: str
    password: str
    queue: str


def load_config() -> NotificationsConfig:
    return NotificationsConfig(
        host=os.getenv("RABBIT_HOST", "213.199.42.57"),
        port=int(os.getenv("RABBIT_PORT", "5672")),
        virtual_host=os.getenv("RABBIT_VHOST", "/"),
        user=os.getenv("RABBIT_USER", "students"),
        password=os.getenv("RABBIT_PASSWORD", "Ut3c2026"),
        queue=os.getenv("NOTIFICATION_QUEUE", "reward.processed"),
    )
