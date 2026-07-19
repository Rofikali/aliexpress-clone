import json
import logging

import pika
from django.core.exceptions import ObjectDoesNotExist
from pydantic import ValidationError

from apps.notifications.services import OrderCreatedNotificationService


logger = logging.getLogger(__name__)


class RabbitMQOrderCreatedConsumer:
    def __init__(self, *, url, queue, connection_factory=None, pika_module=pika):
        self.url = url
        self.queue = queue
        self.pika = pika_module
        self.connection_factory = connection_factory or pika_module.BlockingConnection
        self.service = OrderCreatedNotificationService()

    def consume_forever(self):
        connection = self.connection_factory(self.pika.URLParameters(self.url))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(queue=self.queue, on_message_callback=self._on_message)
        try:
            channel.start_consuming()
        finally:
            connection.close()

    def _on_message(self, channel, method, properties, body):
        try:
            self.service.handle(message=json.loads(body))
        except (ObjectDoesNotExist, ValidationError, json.JSONDecodeError, ValueError):
            logger.exception("order_notification_rejected")
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            logger.exception("order_notification_retry_scheduled")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)
