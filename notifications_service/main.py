import pika

from notifications_service.application.send_notification import (
    SendNotificationUseCase,
)
from notifications_service.config import load_config
from notifications_service.infrastructure.messaging.rabbit_consumer import (
    RabbitNotificationConsumer,
)
from notifications_service.infrastructure.sender.console_sender import (
    ConsoleNotificationSender,
)


def build_consumer() -> RabbitNotificationConsumer:
    config = load_config()
    credentials = pika.PlainCredentials(config.user, config.password)
    params = pika.ConnectionParameters(
        config.host, config.port, config.virtual_host, credentials
    )

    def connection_factory() -> pika.BlockingConnection:
        return pika.BlockingConnection(params)

    sender = ConsoleNotificationSender()
    use_case = SendNotificationUseCase(sender)
    return RabbitNotificationConsumer(connection_factory, config.queue, use_case)


if __name__ == "__main__":
    print(" [*] Notifications service starting...")
    build_consumer().start()
