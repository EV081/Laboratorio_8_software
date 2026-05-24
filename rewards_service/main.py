import pika

from rewards_service.application.process_dinner import ProcessDinnerUseCase
from rewards_service.config import load_config
from rewards_service.domain.policy.points_policy import PercentagePointsPolicy
from rewards_service.infrastructure.messaging.rabbit_consumer import (
    RabbitDinnerConsumer,
)
from rewards_service.infrastructure.messaging.rabbit_notification_publisher import (
    RabbitNotificationPublisher,
)
from rewards_service.infrastructure.persistence.in_memory_repo import (
    InMemoryRewardRepository,
)


def build_consumer() -> RabbitDinnerConsumer:
    config = load_config()
    credentials = pika.PlainCredentials(config.user, config.password)
    params = pika.ConnectionParameters(
        config.host, config.port, config.virtual_host, credentials
    )

    def connection_factory() -> pika.BlockingConnection:
        return pika.BlockingConnection(params)

    repository = InMemoryRewardRepository()
    policy = PercentagePointsPolicy(config.points_percentage)
    notifier = RabbitNotificationPublisher(
        connection_factory, queue=config.notification_queue
    )
    use_case = ProcessDinnerUseCase(repository, policy, notifier)
    return RabbitDinnerConsumer(connection_factory, config.dinner_queue, use_case)


if __name__ == "__main__":
    print(" [*] Rewards service starting...")
    build_consumer().start()
