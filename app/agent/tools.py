import json
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.order import OrderCreate
from app.schemas.review import ProductRatingResponse
from app.services import order_service, review_service


def create_shopping_tools(db: Session) -> list:
    # These tools are the bridge between LangChain and our backend.
    # Each chat request gets tools connected to the current DB session.
    from langchain_core.tools import tool

    @tool
    def search_products(
        query: str,
        max_price: Optional[float] = None,
        is_organic: Optional[bool] = None,
    ) -> str:
        """Search active products by text with optional price and organic filters."""
        products = product_repository.search_products(
            db=db,
            query=query,
            limit=10,
            offset=0,
        )

        filtered_products = []
        for product in products:
            if not product.is_active:
                continue
            if max_price is not None and product.price > max_price:
                continue
            if is_organic is not None and product.is_organic != is_organic:
                continue

            filtered_products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                    "is_organic": product.is_organic,
                    "stock_quantity": product.stock_quantity,
                    "is_active": product.is_active,
                }
            )

        return json.dumps(filtered_products)

    @tool
    def get_rating(product_id: int) -> str:
        """Get average rating and review count for one product."""
        rating = review_service.get_product_rating(db=db, product_id=product_id)
        return ProductRatingResponse(**rating).model_dump_json()

    @tool
    def checkout(
        product_id: int,
        quantity: int,
        customer_name: str,
        customer_email: str,
    ) -> str:
        """Create a one-item order after the user clearly confirms the purchase."""
        try:
            order = order_service.create_order(
                db=db,
                order_data=OrderCreate(
                    customer_name=customer_name,
                    customer_email=customer_email,
                    items=[{"product_id": product_id, "quantity": quantity}],
                ),
            )
            return (
                f"Order created successfully. "
                f"Order ID: {order['id']}. "
                f"Total amount: ${order['total_amount']:.2f}."
            )
        except HTTPException as exc:
            return f"Could not create order: {exc.detail}"

    return [search_products, get_rating, checkout]
