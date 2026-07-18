from datetime import timedelta
from uuid import uuid4

import pytest
from django.utils import timezone

from apps.outbox.dispatcher import OutboxDispatcher
from apps.outbox.models import OutboxEvent
from apps.outbox.repositories import OutboxRepository


class RecordingPublisher:
    def __init__(self):
        self.events = []

    def publish(self, *, event):
        self.events.append(event)


class FailingPublisher:
    def publish(self, *, event):
        raise RuntimeError(f"Broker unavailable for {event.id}")


def create_outbox_event(*, available_at, status=OutboxEvent.Status.PENDING):
    return OutboxEvent.objects.create(
        aggregate_type="order",
        aggregate_id=uuid4(),
        event_type="order.created",
        payload={"order_id": str(uuid4())},
        status=status,
        available_at=available_at,
    )


@pytest.mark.django_db
def test_dispatcher_marks_acknowledged_events_as_published():
    now = timezone.now()
    event = create_outbox_event(available_at=now)
    publisher = RecordingPublisher()
    dispatcher = OutboxDispatcher(OutboxRepository(), clock=lambda: now)

    result = dispatcher.dispatch_available(publisher=publisher)

    event.refresh_from_db()
    assert result.claimed == 1
    assert result.published == 1
    assert publisher.events == [event]
    assert event.status == OutboxEvent.Status.PUBLISHED
    assert event.attempts == 1
    assert event.published_at == now
    assert event.processing_started_at is None


@pytest.mark.django_db
def test_dispatcher_retries_then_marks_terminal_failures():
    now = timezone.now()
    event = create_outbox_event(available_at=now)
    repository = OutboxRepository()
    dispatcher = OutboxDispatcher(
        repository,
        max_attempts=2,
        retry_base_seconds=30,
        clock=lambda: now,
    )

    first_result = dispatcher.dispatch_available(publisher=FailingPublisher())

    event.refresh_from_db()
    assert first_result.retried == 1
    assert event.status == OutboxEvent.Status.PENDING
    assert event.attempts == 1
    assert event.available_at == now + timedelta(seconds=30)
    assert "Broker unavailable" in event.last_error

    retry_time = now + timedelta(seconds=30)
    retry_dispatcher = OutboxDispatcher(
        repository,
        max_attempts=2,
        retry_base_seconds=30,
        clock=lambda: retry_time,
    )
    second_result = retry_dispatcher.dispatch_available(publisher=FailingPublisher())

    event.refresh_from_db()
    assert second_result.failed == 1
    assert event.status == OutboxEvent.Status.FAILED
    assert event.attempts == 2
    assert event.processing_started_at is None


@pytest.mark.django_db
def test_dispatcher_reclaims_expired_processing_lease_before_delivery():
    now = timezone.now()
    event = create_outbox_event(
        available_at=now,
        status=OutboxEvent.Status.PROCESSING,
    )
    event.attempts = 1
    event.processing_started_at = now - timedelta(seconds=301)
    event.save(update_fields=["attempts", "processing_started_at"])
    publisher = RecordingPublisher()
    dispatcher = OutboxDispatcher(
        OutboxRepository(),
        lease_seconds=300,
        clock=lambda: now,
    )

    result = dispatcher.dispatch_available(publisher=publisher)

    event.refresh_from_db()
    assert result.reclaimed == 1
    assert result.published == 1
    assert event.status == OutboxEvent.Status.PUBLISHED
    assert event.attempts == 2
