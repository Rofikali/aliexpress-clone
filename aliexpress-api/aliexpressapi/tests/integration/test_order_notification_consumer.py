from io import StringIO
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone

from apps.notifications.models import Notification
from apps.notifications.services import OrderCreatedNotificationService
from apps.outbox.models import OutboxEvent


User = get_user_model()


def order_created_message(*, event_id, order_id, user_id):
    return {
        "id": str(event_id),
        "event_type": "order.created",
        "aggregate_type": "order",
        "aggregate_id": str(order_id),
        "payload": {
            "order_id": str(order_id),
            "user_id": str(user_id),
            "total_price": "125.00",
        },
    }


@pytest.mark.django_db
def test_order_created_consumer_creates_one_notification_for_duplicate_delivery():
    user = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    event_id = uuid4()
    message = order_created_message(
        event_id=event_id,
        order_id=uuid4(),
        user_id=user.id,
    )
    service = OrderCreatedNotificationService()

    first_notification = service.handle(message=message)
    replayed_notification = service.handle(message=message)

    assert first_notification.id == replayed_notification.id
    assert Notification.objects.filter(event_id=event_id).count() == 1
    assert first_notification.user == user
    assert first_notification.payload["total_price"] == "125.00"


@pytest.mark.django_db
def test_reconciliation_reports_published_order_events_without_notifications():
    event = OutboxEvent.objects.create(
        aggregate_type="order",
        aggregate_id=uuid4(),
        event_type="order.created",
        payload={"order_id": str(uuid4())},
        status=OutboxEvent.Status.PUBLISHED,
        available_at=timezone.now(),
        published_at=timezone.now(),
    )
    output = StringIO()

    call_command("reconcile_order_notifications", stdout=output)

    assert str(event.id) in output.getvalue()
    assert "Missing notification projections: 1" in output.getvalue()
