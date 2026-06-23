from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    # This query finds one product by its primary key.
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_name(db: Session, name: str) -> Optional[Product]:
    # This query checks whether a product with the same name already exists.
    return db.query(Product).filter(func.lower(Product.name) == name.lower()).first()


def get_products(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    category_id: Optional[int] = None,
    is_organic: Optional[bool] = None,
    is_active: Optional[bool] = True,
    max_price: Optional[float] = None,
) -> list[Product]:
    # This query returns products with simple optional filters.
    query = db.query(Product)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if is_organic is not None:
        query = query.filter(Product.is_organic == is_organic)

    if is_active is not None:
        query = query.filter(Product.is_active == is_active)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.offset(offset).limit(limit).all()


def search_products(
    db: Session,
    query: str,
    limit: int = 100,
    offset: int = 0,
) -> list[Product]:
    # This query searches product name and description using ilike.
    search_pattern = f"%{query}%"
    return (
        db.query(Product)
        .filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


def create_product(db: Session, product_data: ProductCreate) -> Product:
    # The repository creates the SQLAlchemy object and saves it.
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:
    # exclude_unset=True updates only the fields the user actually sent.
    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def soft_delete_product(db: Session, product: Product) -> Product:
    # For Phase 4, delete means marking the product as inactive.
    product.is_active = False
    db.commit()
    db.refresh(product)
    return product
