import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.outbox.dispatcher import OutboxDispatcher
from apps.outbox.rabbitmq import RabbitMQPublisher
from apps.outbox.repositories import OutboxRepository


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Dispatch pending outbox events to RabbitMQ."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true")
        parser.add_argument("--batch-size", type=int, default=100)
        parser.add_argument("--poll-seconds", type=int, default=5)

    def handle(self, *args, **options):
        if not settings.RABBITMQ_URL:
            raise CommandError("RABBITMQ_URL must be configured")
        if options["batch_size"] < 1:
            raise CommandError("batch-size must be at least 1")
        if options["poll_seconds"] < 1:
            raise CommandError("poll-seconds must be at least 1")

        publisher = RabbitMQPublisher(
            url=settings.RABBITMQ_URL,
            exchange=settings.RABBITMQ_EXCHANGE,
        )
        dispatcher = OutboxDispatcher(
            OutboxRepository(),
            max_attempts=settings.OUTBOX_MAX_ATTEMPTS,
            retry_base_seconds=settings.OUTBOX_RETRY_BASE_SECONDS,
            lease_seconds=settings.OUTBOX_LEASE_SECONDS,
        )

        while True:
            result = dispatcher.dispatch_available(
                publisher=publisher,
                limit=options["batch_size"],
            )
            logger.info(
                "outbox_dispatch_completed",
                extra={
                    "event": "outbox_dispatch_completed",
                    "claimed": result.claimed,
                    "published": result.published,
                    "retried": result.retried,
                    "failed": result.failed,
                    "reclaimed": result.reclaimed,
                },
            )
            if options["once"]:
                return
            if result.claimed == 0:
                time.sleep(options["poll_seconds"])
