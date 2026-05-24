from abc import ABC, abstractmethod
from typing import Callable

import pika


class BaseRabbitPublisher[T](ABC):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
        exchange: str = "",
    ) -> None:
        self._connection_factory = connection_factory
        self._queue = queue
        self._exchange = exchange

    def publish(self, message: T) -> None:
        payload = self._serialize(message).encode("utf-8")
        connection = self._connection_factory()
        try:
            channel = connection.channel()
            channel.queue_declare(queue=self._queue, durable=True)
            channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._queue,
                body=payload,
                properties=pika.BasicProperties(delivery_mode=2),
            )
        finally:
            connection.close()

    @abstractmethod
    def _serialize(self, message: T) -> str:
        raise NotImplementedError


class BaseRabbitConsumer[T](ABC):
    def __init__(
        self,
        connection_factory: Callable[[], pika.BlockingConnection],
        queue: str,
    ) -> None:
        self._connection_factory = connection_factory
        self._queue = queue

    def start(self) -> None:
        connection = self._connection_factory()
        channel = connection.channel()
        channel.queue_declare(queue=self._queue, durable=True)
        channel.basic_consume(
            queue=self._queue,
            on_message_callback=self.on_message,
            auto_ack=True,
        )
        channel.start_consuming()

    def on_message(self, _channel, _method, _properties, body: bytes) -> None:
        message = self._deserialize(body)
        self._handle(message)

    @abstractmethod
    def _deserialize(self, body: bytes) -> T:
        raise NotImplementedError

    @abstractmethod
    def _handle(self, message: T) -> None:
        raise NotImplementedError
