from django.db import transaction
from apps.outbox.models import OutboxEvent


class OutboxRepository:
    def enqueue(self, *, aggregate_type, aggregate_id, event_type, payload):
        event, _ = OutboxEvent.objects.get_or_create(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            defaults={"payload": payload},
        )
        return event

    def reclaim_expired_claims(self, *, before, available_at):
        return OutboxEvent.objects.filter(
            status=OutboxEvent.Status.PROCESSING,
            processing_started_at__lt=before,
        ).update(
            status=OutboxEvent.Status.PENDING,
            available_at=available_at,
            processing_started_at=None,
            last_error="Processing lease expired",
        )

    def claim_available(self, *, limit, now):
        with transaction.atomic():
            events = list(
                OutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(
                    status=OutboxEvent.Status.PENDING,
                    available_at__lte=now,
                )
                .order_by("available_at", "created_at")[:limit]
            )
            for event in events:
                event.status = OutboxEvent.Status.PROCESSING
                event.attempts += 1
                event.processing_started_at = now
                event.last_error = ""
                event.save(
                    update_fields=[
                        "status",
                        "attempts",
                        "processing_started_at",
                        "last_error",
                    ]
                )
        return events

    def mark_published(self, *, event_id, published_at):
        return OutboxEvent.objects.filter(
            id=event_id,
            status=OutboxEvent.Status.PROCESSING,
        ).update(
            status=OutboxEvent.Status.PUBLISHED,
            processing_started_at=None,
            published_at=published_at,
            last_error="",
        )

    def record_failure(self, *, event_id, error, retry_at, max_attempts):
        with transaction.atomic():
            event = OutboxEvent.objects.select_for_update().get(id=event_id)
            if event.status != OutboxEvent.Status.PROCESSING:
                return event.status

            event.last_error = error[:4000]
            event.processing_started_at = None
            if event.attempts >= max_attempts:
                event.status = OutboxEvent.Status.FAILED
                event.save(
                    update_fields=["status", "processing_started_at", "last_error"]
                )
                return event.status

            event.status = OutboxEvent.Status.PENDING
            event.available_at = retry_at
            event.save(
                update_fields=[
                    "status",
                    "available_at",
                    "processing_started_at",
                    "last_error",
                ]
            )
            return event.status
