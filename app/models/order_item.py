from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OrderItem(Base):
    # This model maps to the order_items table in the database.
    __tablename__ = "order_items"

    # These columns store one line item inside an order.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product_name_snapshot: Mapped[str] = mapped_column(String, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    line_total: Mapped[float] = mapped_column(Float, nullable=False)

    # Each order item belongs to one order.
    order = relationship("Order", back_populates="order_items")

    # Each order item also points to one product.
    product = relationship("Product", back_populates="order_items")
