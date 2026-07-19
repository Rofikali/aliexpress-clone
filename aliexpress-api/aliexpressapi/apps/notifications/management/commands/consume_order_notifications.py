from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.notifications.rabbitmq import RabbitMQOrderCreatedConsumer


class Command(BaseCommand):
    help = "Consume order.created events into buyer notifications."

    def handle(self, *args, **options):
        if not settings.RABBITMQ_URL:
            raise CommandError("RABBITMQ_URL must be configured")
        RabbitMQOrderCreatedConsumer(
            url=settings.RABBITMQ_URL,
            queue="marketplace.notifications.order-created",
        ).consume_forever()
