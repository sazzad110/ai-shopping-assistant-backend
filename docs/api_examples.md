# API Examples

This document collects practical `curl` examples for the main API flows, including the AI assistant.

Base URL used below:

`http://127.0.0.1:8000`

API prefix:

`/api/v1`

## Health Checks

```bash
curl http://127.0.0.1:8000/
```

```bash
curl http://127.0.0.1:8000/api/v1/health
```

## AI Assistant

The chat endpoint is:

`POST /api/v1/chat`

It accepts:

- `message`
- optional `customer_name`
- optional `customer_email`
- optional `history`

### Basic Product Discovery

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I want organic honey under $10 with rating 4"
}'
```

### Recommendation With Checkout Details Included

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "Show me highly rated organic products",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

### Explicit Confirmation Request

This is the kind of message that can allow the agent to use the `checkout` tool if all required details are present.

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I confirm I want to order product ID 1 quantity 2",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

### Follow-Up Chat With History

This example shows how the frontend can send previous messages so the agent can understand follow-up references like "order the first product".

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "history": [
    {
      "role": "user",
      "content": "I want organic honey under $10 with rating 4"
    },
    {
      "role": "assistant",
      "content": "1. Raw Honey (ID: 5) - $9.99 - Rating 4.8/5 - Organic"
    }
  ],
  "message": "I confirm I want to order the first product quantity 2",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

### Expected Chat Behavior

Typical agent tool flow for a product request:

`message`
-> `search_products`
-> `get_rating`
-> assistant recommendation reply

Typical agent tool flow for confirmed ordering:

`message + history`
-> agent resolves the product reference
-> `checkout`
-> order service validation
-> final confirmation reply

## Streamlit Frontend

Run the frontend:

```bash
streamlit run frontend/streamlit_app.py
```

Optional custom backend base URL:

```bash
export FASTAPI_BASE_URL=http://127.0.0.1:8000/api/v1
streamlit run frontend/streamlit_app.py
```

## Categories

### Create Category

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/categories" \
-H "Content-Type: application/json" \
-d '{
  "name": "Dairy",
  "description": "Organic milk, cheese, yogurt, and dairy products"
}'
```

### List And Get Categories

```bash
curl "http://127.0.0.1:8000/api/v1/categories"
curl "http://127.0.0.1:8000/api/v1/categories?limit=10&offset=0"
curl "http://127.0.0.1:8000/api/v1/categories/1"
```

### Update Category

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/categories/1" \
-H "Content-Type: application/json" \
-d '{
  "description": "Updated organic dairy products"
}'
```

### Delete Category

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/categories/1"
```

## Products

### Create Product

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products" \
-H "Content-Type: application/json" \
-d '{
  "name": "Organic Greek Yogurt",
  "category_id": 1,
  "price": 6.99,
  "description": "Creamy organic Greek yogurt",
  "is_organic": true,
  "stock_quantity": 25
}'
```

### Product Listing And Filtering

```bash
curl "http://127.0.0.1:8000/api/v1/products"
curl "http://127.0.0.1:8000/api/v1/products?is_active=true"
curl "http://127.0.0.1:8000/api/v1/products?category_id=1"
curl "http://127.0.0.1:8000/api/v1/products?is_organic=true"
curl "http://127.0.0.1:8000/api/v1/products?max_price=10"
curl "http://127.0.0.1:8000/api/v1/products?limit=5&offset=0"
```

### Product Search And Ratings

```bash
curl "http://127.0.0.1:8000/api/v1/products/search?query=honey"
curl "http://127.0.0.1:8000/api/v1/products/with-ratings"
curl "http://127.0.0.1:8000/api/v1/products/1"
curl "http://127.0.0.1:8000/api/v1/products/1/rating"
```

### Update Product

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/products/1" \
-H "Content-Type: application/json" \
-d '{
  "price": 7.49,
  "stock_quantity": 40
}'
```

### Delete Product

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/products/1"
```

## Reviews

### Create Review

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products/1/reviews" \
-H "Content-Type: application/json" \
-d '{
  "rating": 5,
  "reviewer_name": "Sazzad",
  "review_text": "Fresh and high quality product."
}'
```

### Review Reads

```bash
curl "http://127.0.0.1:8000/api/v1/products/1/reviews"
curl "http://127.0.0.1:8000/api/v1/reviews/1"
```

### Update Review

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/reviews/1" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4,
  "review_text": "Still good, but delivery was a little late."
}'
```

### Delete Review

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/reviews/1"
```

## Orders

### Create Order From Cart-Like Payload

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/orders" \
-H "Content-Type: application/json" \
-d '{
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}'
```

### List And Get Orders

```bash
curl "http://127.0.0.1:8000/api/v1/orders"
curl "http://127.0.0.1:8000/api/v1/orders?limit=10&offset=0"
curl "http://127.0.0.1:8000/api/v1/orders/1"
```

### Update Order Status

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/orders/1/status" \
-H "Content-Type: application/json" \
-d '{
  "status": "confirmed"
}'
```
