from io import StringIO
from uuid import uuid4

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from apps.outbox.models import OutboxEvent


def create_failed_event():
    return OutboxEvent.objects.create(
        aggregate_type="order",
        aggregate_id=uuid4(),
        event_type="order.created",
        payload={"order_id": str(uuid4())},
        status=OutboxEvent.Status.FAILED,
        attempts=5,
        available_at=timezone.now(),
        last_error="Broker unavailable",
    )


@pytest.mark.django_db
def test_replay_command_requeues_one_failed_event_with_audit_details():
    event = create_failed_event()
    output = StringIO()

    call_command(
        "replay_outbox",
        event_id=str(event.id),
        reason="RabbitMQ connectivity restored",
        stdout=output,
    )

    event.refresh_from_db()
    assert "Requeued outbox event" in output.getvalue()
    assert event.status == OutboxEvent.Status.PENDING
    assert event.attempts == 0
    assert event.manual_replay_count == 1
    assert event.last_replay_reason == "RabbitMQ connectivity restored"
    assert event.last_replayed_at is not None
    assert event.last_error == "Broker unavailable"


@pytest.mark.django_db
def test_replay_command_rejects_events_that_are_not_terminal_failures():
    event = create_failed_event()
    event.status = OutboxEvent.Status.PUBLISHED
    event.save(update_fields=["status"])

    with pytest.raises(CommandError, match="Only failed outbox events"):
        call_command(
            "replay_outbox",
            event_id=str(event.id),
            reason="Attempting an unsafe replay",
        )
