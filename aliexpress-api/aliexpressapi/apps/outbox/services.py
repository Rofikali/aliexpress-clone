from apps.outbox.contracts import OrderCreatedEvent
from apps.outbox.repositories import OutboxRepository


class OutboxService:
    def __init__(self, repository: OutboxRepository):
        self.repository = repository

    def record_order_created(self, *, order):
        event = OrderCreatedEvent(
            order_id=order.id,
            user_id=str(order.user_id),
            total_price=str(order.total_price),
        )
        return self.repository.enqueue(
            aggregate_type="order",
            aggregate_id=order.id,
            event_type="order.created",
            payload=event.model_dump(mode="json"),
        )
