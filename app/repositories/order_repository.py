from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate


def create_order_with_items(
    db: Session,
    order_data: OrderCreate,
    validated_items: list[dict],
    total_amount: float,
) -> Order:
    # First we create the order row itself.
    order = Order(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        status="pending",
        total_amount=total_amount,
    )
    db.add(order)

    # flush() sends the insert so SQLAlchemy can give us order.id
    # before we create the related order items.
    db.flush()

    for item in validated_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            product_name_snapshot=item["product_name_snapshot"],
            unit_price=item["unit_price"],
            quantity=item["quantity"],
            line_total=item["line_total"],
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, limit: int = 100, offset: int = 0) -> list[Order]:
    # This query returns a paginated list of orders.
    return db.query(Order).offset(offset).limit(limit).all()


def get_order_by_id(db: Session, order_id: int):
    # This query finds one order by its primary key.
    return db.query(Order).filter(Order.id == order_id).first()


def update_order_status(db: Session, order: Order, status: str) -> Order:
    # This updates only the status field for the order.
    order.status = status
    db.commit()
    db.refresh(order)
    return order
