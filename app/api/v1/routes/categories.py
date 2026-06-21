from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services import category_service


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    # The route receives HTTP data and passes it to the service layer.
    return category_service.create_category(db, category_data)


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    limit: int = Query(default=100, ge=0),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    # Pagination is kept simple for beginner learning.
    return category_service.get_categories(db, limit=limit, offset=offset)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    return category_service.update_category(db, category_id, category_data)


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_service.delete_category(db, category_id)
    return {"message": "Category deleted successfully"}
