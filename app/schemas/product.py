from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    # This base schema contains the shared product fields
    # used by incoming product request bodies.
    name: str
    category_id: int
    price: float = Field(..., ge=0)
    description: Optional[str] = None
    is_organic: bool = True
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    # This create schema is used for the request body
    # when a client creates a new product.
    pass


class ProductUpdate(BaseModel):
    # All fields are optional here so PATCH requests
    # can update only the fields the user sends.
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = Field(default=None, ge=0)
    description: Optional[str] = None
    is_organic: Optional[bool] = None
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    # This response schema defines the product data
    # the API sends back to the client.
    id: int
    name: str
    category_id: int
    price: float
    description: Optional[str]
    is_organic: bool
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # from_attributes=True lets Pydantic read values
    # directly from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)


class ProductWithRatingResponse(ProductResponse):
    # This response is used when the API returns product data
    # together with calculated review rating values.
    average_rating: float
    review_count: int
