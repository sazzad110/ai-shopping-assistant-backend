from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import order_repository, product_repository
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate


def _serialize_order(order) -> dict:
    # The database model uses order_items, but the API response
    # should return the nested list under the name items.
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name_snapshot": item.product_name_snapshot,
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "line_total": item.line_total,
            }
            for item in order.order_items
        ],
    }


def create_order(db: Session, order_data: OrderCreate):
    seen_product_ids = set()
    validated_items = []
    total_amount = 0.0

    for item in order_data.items:
        if item.product_id in seen_product_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate product in order items is not allowed",
            )
        seen_product_ids.add(item.product_id)

        product = product_repository.get_product_by_id(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not active",
            )

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product: {product.name}",
            )

        line_total = product.price * item.quantity
        total_amount += line_total

        # We decrease stock on the SQLAlchemy product object here,
        # but we do not commit yet. SQLAlchemy tracks the change in
        # the same session, and the repository commit will save it.
        product.stock_quantity -= item.quantity

        validated_items.append(
            {
                "product_id": product.id,
                "product_name_snapshot": product.name,
                "unit_price": product.price,
                "quantity": item.quantity,
                "line_total": line_total,
            }
        )

    order = order_repository.create_order_with_items(
        db=db,
        order_data=order_data,
        validated_items=validated_items,
        total_amount=total_amount,
    )
    return _serialize_order(order)


def get_orders(db: Session, limit: int = 100, offset: int = 0):
    orders = order_repository.get_orders(db, limit=limit, offset=offset)
    return [_serialize_order(order) for order in orders]


def get_order(db: Session, order_id: int):
    order = order_repository.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return _serialize_order(order)


def update_order_status(db: Session, order_id: int, status_data: OrderStatusUpdate):
    order = order_repository.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Advanced cancellation logic, such as restoring stock,
    # can be added in a later phase when needed.
    updated_order = order_repository.update_order_status(db, order, status_data.status)
    return _serialize_order(updated_order)
