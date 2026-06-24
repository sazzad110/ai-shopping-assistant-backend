import os
from typing import Any, Dict, List, Optional

import requests


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def _get_api_base_url() -> str:
    # The frontend reads the FastAPI base URL from the environment.
    # If it is missing, we fall back to the local development default.
    return os.getenv("FASTAPI_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def _get_root_base_url() -> str:
    # Some endpoints are under /api/v1 and some helpful checks may use the root.
    # If the configured URL already ends with /api/v1, we remove that part here.
    api_base_url = _get_api_base_url()
    if api_base_url.endswith("/api/v1"):
        return api_base_url[: -len("/api/v1")]
    return api_base_url


def _extract_error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return f"Request failed with status {response.status_code}"

    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and error.get("message"):
            return str(error["message"])
        if payload.get("detail"):
            return str(payload["detail"])

    return f"Request failed with status {response.status_code}"


def _request(
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    use_root_base: bool = False,
) -> Any:
    # All HTTP communication is centralized here so the Streamlit pages
    # stay simple and do not need to manage requests directly.
    base_url = _get_root_base_url() if use_root_base else _get_api_base_url()
    url = f"{base_url}{path}"

    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not connect to backend: {exc}") from exc

    if not response.ok:
        raise RuntimeError(_extract_error_message(response))

    if response.content:
        return response.json()
    return {}


def check_backend_health() -> Dict[str, Any]:
    # We call both the root endpoint and the API health endpoint so the UI
    # can show a more helpful status card on the home page.
    root_data = _request("GET", "/", use_root_base=True)
    health_data = _request("GET", "/health")
    return {
        "root": root_data,
        "health": health_data,
    }


def get_products(params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    return _request("GET", "/products", params=params or {})


def get_products_with_ratings(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    return _request(
        "GET",
        "/products/with-ratings",
        params={"limit": limit, "offset": offset},
    )


def get_product(product_id: int) -> Dict[str, Any]:
    return _request("GET", f"/products/{product_id}")


def get_product_reviews(product_id: int) -> List[Dict[str, Any]]:
    return _request("GET", f"/products/{product_id}/reviews")


def get_product_rating(product_id: int) -> Dict[str, Any]:
    return _request("GET", f"/products/{product_id}/rating")


def create_review(
    product_id: int,
    rating: int,
    reviewer_name: str,
    review_text: Optional[str],
) -> Dict[str, Any]:
    return _request(
        "POST",
        f"/products/{product_id}/reviews",
        json_data={
            "rating": rating,
            "reviewer_name": reviewer_name,
            "review_text": review_text,
        },
    )


def create_order(
    customer_name: str,
    customer_email: str,
    items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return _request(
        "POST",
        "/orders",
        json_data={
            "customer_name": customer_name,
            "customer_email": customer_email,
            "items": items,
        },
    )


def get_orders(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    return _request(
        "GET",
        "/orders",
        params={"limit": limit, "offset": offset},
    )


def update_order_status(order_id: int, status: str) -> Dict[str, Any]:
    return _request(
        "PATCH",
        f"/orders/{order_id}/status",
        json_data={"status": status},
    )


def chat_with_agent(
    message: str,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    return _request(
        "POST",
        "/chat",
        json_data={
            "message": message,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "history": history or [],
        },
    )
