from decimal import Decimal
from typing import List

from notifications_service.application.send_notification import (
    SendNotificationUseCase,
)
from notifications_service.domain.model.notification import Notification
from notifications_service.domain.ports.notification_sender import NotificationSender


class _CapturingSender(NotificationSender):
    def __init__(self) -> None:
        self.sent: List[Notification] = []

    def send(self, notification: Notification) -> None:
        self.sent.append(notification)


def test_use_case_delegates_to_sender():
    sender = _CapturingSender()
    use_case = SendNotificationUseCase(sender)
    notification = Notification("C1", Decimal("10"), Decimal("10"))

    use_case.execute(notification)

    assert sender.sent == [notification]
