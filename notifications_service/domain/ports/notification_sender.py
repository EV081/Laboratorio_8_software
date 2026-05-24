from abc import ABC, abstractmethod

from notifications_service.domain.model.notification import Notification


class NotificationSender(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        raise NotImplementedError
