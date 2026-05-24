from notifications_service.domain.model.notification import Notification
from notifications_service.domain.ports.notification_sender import NotificationSender


class SendNotificationUseCase:
    def __init__(self, sender: NotificationSender) -> None:
        self._sender = sender

    def execute(self, notification: Notification) -> None:
        self._sender.send(notification)
