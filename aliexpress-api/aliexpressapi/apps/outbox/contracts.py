from uuid import UUID

from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    order_id: UUID
    user_id: str
    total_price: str
