from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services import order_service


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # The route receives order data and passes it to the service layer.
    return order_service.create_order(db, order_data)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    limit: int = Query(default=100, ge=0),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    # Pagination is kept simple for beginner learning.
    return order_service.get_orders(db, limit=limit, offset=offset)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    return order_service.update_order_status(db, order_id, status_data)
