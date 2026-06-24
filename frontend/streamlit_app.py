from typing import Any, Dict, List

import streamlit as st

import api_client
from ui_helpers import (
    format_price,
    format_rating,
    product_card,
    show_error,
    show_success,
)


st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide",
)


def initialize_session_state() -> None:
    st.session_state.setdefault("cart", {})
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("selected_product_id", None)
    st.session_state.setdefault("customer_name", "")
    st.session_state.setdefault("customer_email", "")


def add_to_cart(product: Dict[str, Any]) -> None:
    cart = st.session_state.cart
    product_id = int(product["id"])

    if product_id in cart:
        cart[product_id]["quantity"] += 1
    else:
        cart[product_id] = {
            "product_id": product_id,
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": 1,
            "stock_quantity": int(product.get("stock_quantity", 0)),
        }


def render_home_page() -> None:
    st.title("AI Shopping Assistant")
    st.caption("Organic grocery shopping powered by FastAPI and AI")

    left_col, right_col = st.columns([1.3, 1])

    with left_col:
        st.subheader("Project Overview")
        st.write(
            """
            This frontend talks to a FastAPI backend that handles products,
            reviews, ratings, orders, and an AI shopping assistant.
            """
        )
        st.write(
            """
            Use the sidebar to browse products, add items to cart,
            place orders, or chat with the AI assistant.
            """
        )

    with right_col:
        st.subheader("Backend Status")
        try:
            health_data = api_client.check_backend_health()
            st.success("Backend is online")
            st.write(f"Root: {health_data['root'].get('message', 'OK')}")
            st.write(f"API Health: {health_data['health'].get('message', 'OK')}")
        except Exception as exc:
            st.error("Backend is offline")
            st.write(str(exc))

    st.subheader("What is included")
    info_cols = st.columns(4)
    info_cols[0].info("FastAPI backend")
    info_cols[1].info("SQLAlchemy database")
    info_cols[2].info("Reviews and ratings")
    info_cols[3].info("LangChain/Groq AI assistant")

    st.subheader("Quick Navigation Tips")
    st.write("- Products: browse items, ratings, and reviews")
    st.write("- Cart / Order: manage cart and place orders")
    st.write("- AI Assistant: ask for recommendations or order help")
    st.write("- Orders: review recent orders and update status")


def render_products_page() -> None:
    st.title("Products")
    st.caption("Browse available organic grocery products")

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    search_text = filter_col1.text_input("Search text")
    organic_only = filter_col2.checkbox("Organic only")
    max_price = filter_col3.number_input("Max price", min_value=0.0, value=0.0, step=1.0)
    active_only = filter_col4.checkbox("Active products only", value=True)

    try:
        products = api_client.get_products_with_ratings(limit=100, offset=0)
    except Exception as exc:
        show_error(str(exc))
        return

    # For beginner learning, extra filtering is applied in Streamlit after
    # loading product data from the backend. For large production datasets,
    # backend-side filtering should remain the preferred approach.
    filtered_products: List[Dict[str, Any]] = []
    for product in products:
        if search_text:
            combined_text = f"{product.get('name', '')} {product.get('description', '')}".lower()
            if search_text.lower() not in combined_text:
                continue
        if organic_only and not product.get("is_organic"):
            continue
        if active_only and not product.get("is_active"):
            continue
        if max_price > 0 and float(product.get("price", 0)) > max_price:
            continue
        filtered_products.append(product)

    if not filtered_products:
        st.info("No products found with the current filters.")
        return

    for row_start in range(0, len(filtered_products), 3):
        columns = st.columns(3)
        row_items = filtered_products[row_start : row_start + 3]

        for column, product in zip(columns, row_items):
            with column:
                st.container(border=True)
                product_card(product)

                add_key = f"add_to_cart_{product['id']}"
                if st.button("Add to cart", key=add_key, use_container_width=True):
                    add_to_cart(product)
                    show_success(f"Added {product['name']} to cart")

                with st.expander("View reviews and rating"):
                    try:
                        rating = api_client.get_product_rating(int(product["id"]))
                        reviews = api_client.get_product_reviews(int(product["id"]))
                    except Exception as exc:
                        show_error(str(exc))
                        rating = {"average_rating": 0.0, "review_count": 0}
                        reviews = []

                    st.write(
                        f"Rating: {format_rating(float(rating['average_rating']), int(rating['review_count']))}"
                    )

                    if reviews:
                        for review in reviews:
                            st.write(
                                f"- {review['reviewer_name']} rated {review['rating']}/5: "
                                f"{review.get('review_text') or 'No comment'}"
                            )
                    else:
                        st.info("No reviews yet.")

                with st.expander("Add review"):
                    reviewer_name = st.text_input(
                        "Reviewer name",
                        key=f"reviewer_name_{product['id']}",
                    )
                    review_rating = st.selectbox(
                        "Rating",
                        options=[1, 2, 3, 4, 5],
                        index=4,
                        key=f"review_rating_{product['id']}",
                    )
                    review_text = st.text_area(
                        "Review text",
                        key=f"review_text_{product['id']}",
                    )

                    submit_key = f"submit_review_{product['id']}"
                    if st.button("Submit review", key=submit_key):
                        if not reviewer_name.strip():
                            show_error("Reviewer name is required.")
                        else:
                            try:
                                api_client.create_review(
                                    product_id=int(product["id"]),
                                    rating=int(review_rating),
                                    reviewer_name=reviewer_name.strip(),
                                    review_text=review_text.strip() or None,
                                )
                                show_success("Review submitted successfully.")
                            except Exception as exc:
                                show_error(str(exc))


def render_cart_page() -> None:
    st.title("Cart / Order")
    st.caption("Review your cart and place an order")

    st.session_state.customer_name = st.text_input(
        "Customer name",
        value=st.session_state.customer_name,
    )
    st.session_state.customer_email = st.text_input(
        "Customer email",
        value=st.session_state.customer_email,
    )

    cart = st.session_state.cart
    if not cart:
        st.info("Your cart is empty.")
        return

    estimated_total = 0.0
    items_to_remove = []

    for product_id, item in cart.items():
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2.5, 1.2, 1.2, 1])
            col1.write(f"**{item['name']}** (ID: {item['product_id']})")
            col2.write(f"Price: {format_price(item['price'])}")

            new_quantity = col3.number_input(
                "Quantity",
                min_value=1,
                max_value=max(1, item["stock_quantity"]),
                value=item["quantity"],
                step=1,
                key=f"cart_quantity_{product_id}",
            )
            item["quantity"] = int(new_quantity)

            if col4.button("Remove", key=f"remove_{product_id}"):
                items_to_remove.append(product_id)

            line_total = item["price"] * item["quantity"]
            estimated_total += line_total
            st.caption(f"Estimated line total: {format_price(line_total)}")

    for product_id in items_to_remove:
        cart.pop(product_id, None)

    if not cart:
        st.info("Your cart is empty.")
        return

    st.subheader(f"Estimated total: {format_price(estimated_total)}")
    st.caption("The backend calculates the final trusted order total.")

    if st.button("Place order", type="primary"):
        if not st.session_state.customer_name.strip():
            show_error("Customer name is required.")
            return
        if not st.session_state.customer_email.strip():
            show_error("Customer email is required.")
            return

        items = [
            {"product_id": item["product_id"], "quantity": item["quantity"]}
            for item in cart.values()
        ]

        try:
            order = api_client.create_order(
                customer_name=st.session_state.customer_name.strip(),
                customer_email=st.session_state.customer_email.strip(),
                items=items,
            )
            show_success(
                f"Order placed successfully. Order ID: {order['id']}. "
                f"Total: {format_price(float(order['total_amount']))}"
            )
            st.session_state.cart = {}
        except Exception as exc:
            show_error(str(exc))


def render_ai_page() -> None:
    st.title("AI Assistant")
    st.caption("Ask the shopping assistant about products, ratings, or orders")

    with st.sidebar:
        st.subheader("Chat Checkout Details")
        st.session_state.customer_name = st.text_input(
            "Customer name",
            value=st.session_state.customer_name,
            key="chat_customer_name",
        )
        st.session_state.customer_email = st.text_input(
            "Customer email",
            value=st.session_state.customer_email,
            key="chat_customer_email",
        )

    st.info("Suggested prompts:")
    st.write('- "I want organic honey under $20 with 4.5+ rating"')
    st.write('- "Show me highly rated organic products"')
    st.write('- "I want to order product ID 1 quantity 2"')
    st.write('- "I confirm I want to order product ID 1 quantity 2"')

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input("Ask the AI shopping assistant")
    if not user_prompt:
        return

    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    history = st.session_state.chat_messages[:-1]
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = api_client.chat_with_agent(
                    message=user_prompt,
                    customer_name=st.session_state.customer_name.strip() or None,
                    customer_email=st.session_state.customer_email.strip() or None,
                    history=history,
                )
                assistant_reply = response["reply"]
                st.write(assistant_reply)
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )
            except Exception as exc:
                error_message = str(exc)
                st.write(error_message)
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": error_message}
                )


def render_orders_page() -> None:
    st.title("Orders")
    st.caption("View recent orders and optionally update status")

    try:
        orders = api_client.get_orders(limit=100, offset=0)
    except Exception as exc:
        show_error(str(exc))
        return

    if not orders:
        st.info("No orders yet.")
        return

    status_options = ["pending", "confirmed", "shipped", "delivered", "cancelled"]

    for order in orders:
        with st.container(border=True):
            st.subheader(f"Order #{order['id']}")
            top_left, top_right = st.columns(2)
            top_left.write(f"Customer: {order['customer_name']}")
            top_left.write(f"Email: {order['customer_email']}")
            top_right.write(f"Status: {order['status']}")
            top_right.write(f"Total: {format_price(float(order['total_amount']))}")
            st.caption(f"Created at: {order['created_at']}")

            with st.expander("Order items"):
                for item in order.get("items", []):
                    st.write(
                        f"- {item['product_name_snapshot']} "
                        f"(ID: {item['product_id']}) x {item['quantity']} "
                        f"= {format_price(float(item['line_total']))}"
                    )

            selected_status = st.selectbox(
                "Update status",
                options=status_options,
                index=status_options.index(order["status"])
                if order["status"] in status_options
                else 0,
                key=f"order_status_{order['id']}",
            )

            if st.button("Save status", key=f"save_status_{order['id']}"):
                try:
                    api_client.update_order_status(order_id=int(order["id"]), status=selected_status)
                    show_success(f"Order #{order['id']} updated successfully.")
                except Exception as exc:
                    show_error(str(exc))


def main() -> None:
    initialize_session_state()

    with st.sidebar:
        st.title("🛒 Navigation")
        page = st.radio(
            "Go to",
            ["Home", "Products", "Cart / Order", "AI Assistant", "Orders"],
        )

    if page == "Home":
        render_home_page()
    elif page == "Products":
        render_products_page()
    elif page == "Cart / Order":
        render_cart_page()
    elif page == "AI Assistant":
        render_ai_page()
    else:
        render_orders_page()


if __name__ == "__main__":
    main()
