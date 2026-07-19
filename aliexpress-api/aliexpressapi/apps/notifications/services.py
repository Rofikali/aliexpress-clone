from django.contrib.auth import get_user_model
from django.db import transaction

from apps.notifications.contracts import OrderCreatedBrokerEvent
from apps.notifications.models import Notification


class OrderCreatedNotificationService:
    @transaction.atomic
    def handle(self, *, message):
        event = OrderCreatedBrokerEvent.model_validate(message)
        user = get_user_model().objects.get(id=event.payload.user_id)
        notification, _ = Notification.objects.get_or_create(
            event_id=event.id,
            defaults={
                "user": user,
                "notification_type": event.event_type,
                "payload": event.payload.model_dump(mode="json"),
            },
        )
        return notification
