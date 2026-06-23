from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    # This nested schema represents one product inside
    # the order request body.
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    # This create schema is used when a client sends
    # a new order with customer details and items.
    customer_name: str
    customer_email: str
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    # This response schema shows one saved item inside an order.
    id: int
    product_id: int
    product_name_snapshot: str
    unit_price: float
    quantity: int
    line_total: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    # This response schema returns full order data
    # together with the nested list of saved order items.
    id: int
    customer_name: str
    customer_email: str
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    # This schema is used when a client updates only the order status.
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
