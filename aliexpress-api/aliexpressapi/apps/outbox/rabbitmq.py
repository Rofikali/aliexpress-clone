import json

import pika


class RabbitMQPublisher:
    def __init__(
        self,
        *,
        url,
        exchange,
        connection_factory=None,
        pika_module=pika,
    ):
        self.url = url
        self.exchange = exchange
        self.pika = pika_module
        self.connection_factory = connection_factory or pika_module.BlockingConnection

    def publish(self, *, event):
        connection = self.connection_factory(self.pika.URLParameters(self.url))
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange,
                exchange_type="topic",
                durable=True,
            )
            channel.confirm_delivery()
            delivered = channel.basic_publish(
                exchange=self.exchange,
                routing_key=event.event_type,
                body=json.dumps(self._message(event), separators=(",", ":")),
                properties=self.pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2,
                    message_id=str(event.id),
                    type=event.event_type,
                ),
                mandatory=True,
            )
            if delivered is False:
                raise RuntimeError("RabbitMQ did not confirm message delivery")
        finally:
            connection.close()

    def _message(self, event):
        return {
            "id": str(event.id),
            "event_type": event.event_type,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": str(event.aggregate_id),
            "payload": event.payload,
            "created_at": event.created_at.isoformat(),
        }
