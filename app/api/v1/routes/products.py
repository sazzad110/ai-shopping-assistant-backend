from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    # The route receives product data and passes it to the service layer.
    return product_service.create_product(db, product_data)


@router.get("", response_model=list[ProductResponse])
def list_products(
    limit: int = Query(default=100, ge=0),
    offset: int = Query(default=0, ge=0),
    category_id: Optional[int] = Query(default=None),
    is_organic: Optional[bool] = Query(default=None),
    is_active: Optional[bool] = Query(default=True),
    max_price: Optional[float] = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    # Filters and pagination are kept simple for beginner learning.
    return product_service.get_products(
        db,
        limit=limit,
        offset=offset,
        category_id=category_id,
        is_organic=is_organic,
        is_active=is_active,
        max_price=max_price,
    )


@router.get("/search", response_model=list[ProductResponse])
def search_products(
    query: str,
    limit: int = Query(default=100, ge=0),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return product_service.search_products(db, query=query, limit=limit, offset=offset)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    return product_service.update_product(db, product_id, product_data)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}
