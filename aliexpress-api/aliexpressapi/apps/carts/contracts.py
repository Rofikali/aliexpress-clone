from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AddCartItemCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_variant_id: UUID
    quantity: Annotated[int, Field(gt=0, strict=True)] = 1
