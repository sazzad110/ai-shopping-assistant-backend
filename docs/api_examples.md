# API Examples

This file collects example `curl` commands for the main API domains.

## Health

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/v1/health
```

## Chat

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I want organic honey under $20 with 4.5+ rating"
}'
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I want to buy honey"
}'
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I confirm I want to order product ID 1 quantity 2",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "history": [
    {
      "role": "user",
      "content": "I want organic honey under $20"
    },
    {
      "role": "assistant",
      "content": "#1. Raw Honey (ID: 5) - $12.99 - rating 4.8. Would you like to order it?"
    }
  ],
  "message": "yes, order quantity 1",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

## Categories

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/categories" \
-H "Content-Type: application/json" \
-d '{
  "name": "Dairy",
  "description": "Organic milk, cheese, yogurt, and dairy products"
}'
```

```bash
curl "http://127.0.0.1:8000/api/v1/categories"
curl "http://127.0.0.1:8000/api/v1/categories?limit=10&offset=0"
curl "http://127.0.0.1:8000/api/v1/categories/1"
```

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/categories/1" \
-H "Content-Type: application/json" \
-d '{
  "description": "Updated organic dairy products"
}'
```

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/categories/1"
```

## Products

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

```bash
curl "http://127.0.0.1:8000/api/v1/products"
curl "http://127.0.0.1:8000/api/v1/products?is_active=true"
curl "http://127.0.0.1:8000/api/v1/products?category_id=1"
curl "http://127.0.0.1:8000/api/v1/products?is_organic=true"
curl "http://127.0.0.1:8000/api/v1/products?max_price=10"
curl "http://127.0.0.1:8000/api/v1/products?limit=5&offset=0"
curl "http://127.0.0.1:8000/api/v1/products/search?query=honey"
curl "http://127.0.0.1:8000/api/v1/products/with-ratings"
curl "http://127.0.0.1:8000/api/v1/products/1"
curl "http://127.0.0.1:8000/api/v1/products/1/rating"
```

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/products/1" \
-H "Content-Type: application/json" \
-d '{
  "price": 7.49,
  "stock_quantity": 40
}'
```

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/products/1"
```

## Reviews

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products/1/reviews" \
-H "Content-Type: application/json" \
-d '{
  "rating": 5,
  "reviewer_name": "Sazzad",
  "review_text": "Fresh and high quality product."
}'
```

```bash
curl "http://127.0.0.1:8000/api/v1/products/1/reviews"
curl "http://127.0.0.1:8000/api/v1/reviews/1"
```

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/reviews/1" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4,
  "review_text": "Still good, but delivery was a little late."
}'
```

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/reviews/1"
```

## Orders

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

```bash
curl "http://127.0.0.1:8000/api/v1/orders"
curl "http://127.0.0.1:8000/api/v1/orders?limit=10&offset=0"
curl "http://127.0.0.1:8000/api/v1/orders/1"
```

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/orders/1/status" \
-H "Content-Type: application/json" \
-d '{
  "status": "confirmed"
}'
```
