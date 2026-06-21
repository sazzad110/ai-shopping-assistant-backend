from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Review(Base):
    # This model maps to the reviews table in the database.
    __tablename__ = "reviews"

    # These columns store review details for a product.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    reviewer_name: Mapped[str] = mapped_column(String, nullable=False)
    review_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Each review belongs to one product.
    product = relationship("Product", back_populates="reviews")
