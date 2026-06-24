from typing import Any, Dict

import streamlit as st


def format_price(value: float) -> str:
    return f"${value:.2f}"


def format_rating(value: float, count: int) -> str:
    if count <= 0:
        return "No reviews yet"
    return f"{value:.1f}★ ({count} reviews)"


def show_error(message: str) -> None:
    st.error(message)


def show_success(message: str) -> None:
    st.success(message)


def product_card(product: Dict[str, Any]) -> None:
    # This helper renders one clean, readable product summary block.
    organic_label = "Organic" if product.get("is_organic") else "Non-organic"
    st.markdown(f"### {product.get('name', 'Unknown Product')}")
    st.caption(f"ID: {product.get('id', '-')}")
    st.write(f"Price: {format_price(float(product.get('price', 0)))}")
    st.write(f"Type: {organic_label}")
    st.write(f"Stock: {product.get('stock_quantity', 0)}")

    average_rating = float(product.get("average_rating", 0.0))
    review_count = int(product.get("review_count", 0))
    st.write(f"Rating: {format_rating(average_rating, review_count)}")

    description = product.get("description") or "No description available."
    st.write(description)
