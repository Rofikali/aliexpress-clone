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
