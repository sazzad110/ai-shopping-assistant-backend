from typing import Optional

from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    # This query finds one category by its primary key.
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    # This query checks whether a category name already exists.
    return db.query(Category).filter(Category.name == name).first()


def get_categories(db: Session, limit: int = 100, offset: int = 0) -> list[Category]:
    # This query returns a paginated list of categories.
    return db.query(Category).offset(offset).limit(limit).all()


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    # The repository creates the SQLAlchemy model and saves it.
    category = Category(
        name=category_data.name,
        description=category_data.description,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate,
) -> Category:
    # exclude_unset=True makes sure we update only fields the user actually sent.
    update_data = category_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    # For Phase 3, we use a simple hard delete.
    db.delete(category)
    db.commit()
