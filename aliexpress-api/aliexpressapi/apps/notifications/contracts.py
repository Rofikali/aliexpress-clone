from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from apps.outbox.contracts import OrderCreatedEvent


class OrderCreatedBrokerEvent(BaseModel):
    id: UUID
    event_type: Literal["order.created"]
    aggregate_type: Literal["order"]
    aggregate_id: UUID
    payload: OrderCreatedEvent
