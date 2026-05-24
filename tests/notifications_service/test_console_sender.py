from decimal import Decimal
from typing import List

from notifications_service.domain.model.notification import Notification
from notifications_service.infrastructure.sender.console_sender import (
    ConsoleNotificationSender,
)


def test_console_sender_writes_message():
    captured: List[str] = []
    sender = ConsoleNotificationSender(writer=captured.append)
    notification = Notification("4111111111111234", Decimal("10"), Decimal("50"))

    sender.send(notification)

    assert len(captured) == 1
    assert "1234" in captured[0]
    assert "10" in captured[0]


def test_console_sender_uses_print_by_default(capsys):
    sender = ConsoleNotificationSender()
    sender.send(Notification("C1", Decimal("1"), Decimal("1")))
    out = capsys.readouterr().out
    assert "C1" in out
