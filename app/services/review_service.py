from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import product_repository, review_repository


def create_review(db: Session, product_id: int, review_data):
    # A review must belong to a real product, so we validate it first.
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return review_repository.create_review(db, product_id, review_data)


def get_reviews_by_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return review_repository.get_reviews_by_product_id(db, product_id)


def get_review(db: Session, review_id: int):
    review = review_repository.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review


def update_review(db: Session, review_id: int, review_data):
    review = review_repository.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review_repository.update_review(db, review, review_data)


def delete_review(db: Session, review_id: int):
    review = review_repository.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    review_repository.delete_review(db, review)


def get_product_rating(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    rating_data = review_repository.get_product_rating(db, product_id)
    return {
        "product_id": product_id,
        "average_rating": rating_data["average_rating"],
        "review_count": rating_data["review_count"],
    }
