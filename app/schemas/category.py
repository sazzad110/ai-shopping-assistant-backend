from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    # This is the shared base schema for category request data.
    # It contains the fields a user can send when working with categories.
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    # This request schema is used when creating a new category.
    pass


class CategoryUpdate(BaseModel):
    # Update fields are optional so the user can send only the values
    # they want to change in a PATCH request.
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    # This response schema defines what the API sends back to the client.
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    # from_attributes=True allows Pydantic to read data directly
    # from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)
