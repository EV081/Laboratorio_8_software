import os

import pika
import uvicorn

from restaurant_service.application.register_dinner import RegisterDinnerUseCase
from restaurant_service.config import load_config
from restaurant_service.infrastructure.messaging.rabbit_publisher import (
    RabbitDinnerPublisher,
)
from restaurant_service.infrastructure.rest.api import create_app


def build_app():
    config = load_config()
    credentials = pika.PlainCredentials(config.user, config.password)
    params = pika.ConnectionParameters(
        config.host, config.port, config.virtual_host, credentials
    )

    def connection_factory() -> pika.BlockingConnection:
        return pika.BlockingConnection(params)

    publisher = RabbitDinnerPublisher(connection_factory, queue=config.queue)
    use_case = RegisterDinnerUseCase(publisher)
    return create_app(use_case)


if __name__ == "__main__":
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(build_app(), host=api_host, port=api_port)
