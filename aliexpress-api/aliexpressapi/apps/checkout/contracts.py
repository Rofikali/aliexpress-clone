from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CheckoutCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    idempotency_key: UUID
