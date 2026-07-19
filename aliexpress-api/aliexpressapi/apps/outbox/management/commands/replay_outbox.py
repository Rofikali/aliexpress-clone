import logging
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError

from apps.outbox.errors import OutboxReplayError
from apps.outbox.repositories import OutboxRepository


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Requeue one failed outbox event after the failure is remediated."

    def add_arguments(self, parser):
        parser.add_argument("--event-id", required=True)
        parser.add_argument("--reason", required=True)

    def handle(self, *args, **options):
        reason = options["reason"].strip()
        if not reason:
            raise CommandError("reason must not be empty")
        if len(reason) > 512:
            raise CommandError("reason must not exceed 512 characters")

        try:
            event_id = UUID(options["event_id"])
        except ValueError as error:
            raise CommandError("event-id must be a UUID") from error

        try:
            event = OutboxRepository().requeue_failed(
                event_id=event_id,
                reason=reason,
            )
        except OutboxReplayError as error:
            raise CommandError(str(error)) from error

        logger.warning(
            "outbox_event_requeued",
            extra={
                "event": "outbox_event_requeued",
                "outbox_event_id": str(event.id),
                "event_type": event.event_type,
                "replay_reason": reason,
                "manual_replay_count": event.manual_replay_count,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Requeued outbox event {event.id}"))
