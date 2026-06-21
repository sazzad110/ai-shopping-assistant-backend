from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category_data: CategoryCreate):
    # The service layer handles business rules before saving data.
    existing_category = category_repository.get_category_by_name(db, category_data.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    return category_repository.create_category(db, category_data)


def get_categories(db: Session, limit: int = 100, offset: int = 0):
    return category_repository.get_categories(db, limit=limit, offset=offset)


def get_category(db: Session, category_id: int):
    category = category_repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    category = category_repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if category_data.name is not None:
        existing_category = category_repository.get_category_by_name(db, category_data.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists",
            )

    return category_repository.update_category(db, category, category_data)


def delete_category(db: Session, category_id: int):
    category = category_repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    try:
        category_repository.delete_category(db, category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category cannot be deleted because it has related products",
        ) from None
