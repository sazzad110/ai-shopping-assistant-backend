from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services import review_service


router = APIRouter(tags=["Reviews"])


@router.post(
    "/products/{product_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    product_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
):
    # The route receives review data and passes it to the service layer.
    return review_service.create_review(db, product_id, review_data)


@router.get("/products/{product_id}/reviews", response_model=list[ReviewResponse])
def list_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    return review_service.get_reviews_by_product(db, product_id)


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.get_review(db, review_id)


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
):
    return review_service.update_review(db, review_id, review_data)


@router.delete("/reviews/{review_id}", response_model=MessageResponse)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_service.delete_review(db, review_id)
    return {"message": "Review deleted successfully"}
