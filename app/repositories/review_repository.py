from typing import Dict, Union

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


def get_review_by_id(db: Session, review_id: int):
    # This query finds one review by its primary key.
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews_by_product_id(db: Session, product_id: int) -> list[Review]:
    # This query returns all reviews that belong to one product.
    return db.query(Review).filter(Review.product_id == product_id).all()


def create_review(db: Session, product_id: int, review_data: ReviewCreate) -> Review:
    # The repository creates the SQLAlchemy review object and saves it.
    review = Review(product_id=product_id, **review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(db: Session, review: Review, review_data: ReviewUpdate) -> Review:
    # exclude_unset=True updates only the fields the user actually sent.
    update_data = review_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review: Review) -> None:
    # For reviews, delete means removing the row from the table.
    db.delete(review)
    db.commit()


def get_product_rating(db: Session, product_id: int) -> Dict[str, Union[float, int]]:
    # This query calculates the average rating and total review count.
    average_rating, review_count = (
        db.query(func.avg(Review.rating), func.count(Review.id))
        .filter(Review.product_id == product_id)
        .one()
    )

    return {
        "average_rating": float(average_rating) if average_rating is not None else 0.0,
        "review_count": review_count,
    }
