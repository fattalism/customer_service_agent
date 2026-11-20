from pydantic import BaseModel, Field, computed_field, ConfigDict
from typing import Annotated


class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)


class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str
    items: Annotated[list[OrderItem], Field(min_length=1)]


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total: int


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    arguments: dict


class GetOrderDetailsArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_id: str


class CancelOrderArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_id: str
