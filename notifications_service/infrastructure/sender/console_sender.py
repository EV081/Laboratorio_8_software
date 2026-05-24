from typing import Callable

from notifications_service.domain.model.notification import Notification
from notifications_service.domain.ports.notification_sender import NotificationSender


class ConsoleNotificationSender(NotificationSender):
    def __init__(self, writer: Callable[[str], None] = print) -> None:
        self._writer = writer

    def send(self, notification: Notification) -> None:
        self._writer(f" [✉] {notification.message()}")
