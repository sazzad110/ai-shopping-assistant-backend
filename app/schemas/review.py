from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    # This base schema contains the shared fields
    # used when a client sends review data.
    rating: int = Field(..., ge=1, le=5)
    reviewer_name: str
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    # This create schema is used for the request body
    # when a client creates a new review.
    pass


class ReviewUpdate(BaseModel):
    # All fields are optional here so PATCH requests
    # can update only the values sent by the user.
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    reviewer_name: Optional[str] = None
    review_text: Optional[str] = None


class ReviewResponse(BaseModel):
    # This response schema defines the review data
    # returned by the API.
    id: int
    product_id: int
    rating: int
    reviewer_name: str
    review_text: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductRatingResponse(BaseModel):
    # This schema is used for rating summary responses.
    # It contains calculated values instead of raw review rows.
    product_id: int
    average_rating: float
    review_count: int
