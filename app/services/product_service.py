from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import category_repository, product_repository
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate):
    # A product must belong to a real category, so we validate it first.
    category = category_repository.get_category_by_id(db, product_data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    cleaned_name = product_data.name.strip()
    existing_product = product_repository.get_product_by_name(db, cleaned_name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already created",
        )

    product_data = product_data.model_copy(update={"name": cleaned_name})
    return product_repository.create_product(db, product_data)


def get_products(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    category_id: Optional[int] = None,
    is_organic: Optional[bool] = None,
    is_active: Optional[bool] = True,
    max_price: Optional[float] = None,
):
    return product_repository.get_products(
        db,
        limit=limit,
        offset=offset,
        category_id=category_id,
        is_organic=is_organic,
        is_active=is_active,
        max_price=max_price,
    )


def search_products(db: Session, query: str, limit: int = 100, offset: int = 0):
    cleaned_query = query.strip()
    if not cleaned_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query cannot be empty",
        )

    return product_repository.search_products(
        db,
        query=cleaned_query,
        limit=limit,
        offset=offset,
    )


def get_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if product_data.category_id is not None:
        category = category_repository.get_category_by_id(db, product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    if product_data.name is not None:
        cleaned_name = product_data.name.strip()
        existing_product = product_repository.get_product_by_name(db, cleaned_name)
        if existing_product and existing_product.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already created",
            )
        product_data = product_data.model_copy(update={"name": cleaned_name})

    return product_repository.update_product(db, product, product_data)


def delete_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product_repository.soft_delete_product(db, product)


def get_products_with_ratings(db: Session, limit: int = 100, offset: int = 0):
    # This helper returns product data together with calculated rating values.
    return product_repository.get_products_with_ratings(db, limit=limit, offset=offset)
