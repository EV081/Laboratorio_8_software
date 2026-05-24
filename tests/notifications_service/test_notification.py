from decimal import Decimal

import pytest

from notifications_service.domain.model.notification import Notification


def test_notification_message_includes_points():
    notification = Notification("4111111111111234", Decimal("10"), Decimal("50"))
    assert "10" in notification.message()
    assert "50" in notification.message()


def test_notification_masks_card_number():
    notification = Notification("4111111111111234", Decimal("1"), Decimal("1"))
    assert notification.masked_card() == "************1234"


def test_short_card_is_not_masked():
    notification = Notification("12", Decimal("1"), Decimal("1"))
    assert notification.masked_card() == "12"


def test_rejects_empty_card():
    with pytest.raises(ValueError):
        Notification("", Decimal("1"), Decimal("1"))


def test_rejects_negative_points_added():
    with pytest.raises(ValueError):
        Notification("C1", Decimal("-1"), Decimal("1"))


def test_rejects_negative_total_points():
    with pytest.raises(ValueError):
        Notification("C1", Decimal("1"), Decimal("-1"))
