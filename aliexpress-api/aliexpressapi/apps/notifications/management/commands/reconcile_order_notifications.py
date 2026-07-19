from django.core.management.base import BaseCommand

from apps.notifications.models import Notification
from apps.outbox.models import OutboxEvent


class Command(BaseCommand):
    help = "Report published order.created events without a notification projection."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        event_ids = Notification.objects.values("event_id")
        missing_events = OutboxEvent.objects.filter(
            event_type="order.created",
            status=OutboxEvent.Status.PUBLISHED,
        ).exclude(id__in=event_ids).order_by("published_at")[: options["limit"]]
        for event in missing_events:
            self.stdout.write(str(event.id))
        self.stdout.write(f"Missing notification projections: {len(missing_events)}")
