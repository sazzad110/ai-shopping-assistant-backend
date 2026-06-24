# AI Shopping Assistant Backend

Portfolio-ready FastAPI backend for an organic grocery shopping assistant.  
This project focuses on clean backend architecture, SQLAlchemy ORM, validation with Pydantic, and business logic that is ready for later AI integration.

Current phase: **Phase 7 - Backend Quality Improvements**

## What This Backend Does

- manages categories
- manages products with filters, search, and soft delete
- manages reviews and rating aggregation
- creates orders with multiple items
- validates stock before order creation
- updates order status
- standardizes API error responses

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy ORM
- SQLite
- Pydantic and Pydantic Settings
- python-dotenv

## Features Completed So Far

- FastAPI project foundation
- environment-based settings
- SQLAlchemy models and automatic local table creation
- Category CRUD
- Product CRUD
- Product search and filters
- Product soft delete
- Review CRUD
- Product rating aggregation
- Order creation with stock validation
- Order listing and status updates
- centralized error handling
- reusable delete response schema

## Folder Structure

```text
app/
├── api/
│   └── v1/
│       ├── router.py
│       └── routes/
│           ├── categories.py
│           ├── health.py
│           ├── orders.py
│           ├── products.py
│           └── reviews.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── exceptions.py
├── models/
│   ├── category.py
│   ├── order.py
│   ├── order_item.py
│   ├── product.py
│   └── review.py
├── repositories/
│   ├── category_repository.py
│   ├── order_repository.py
│   ├── product_repository.py
│   └── review_repository.py
├── schemas/
│   ├── category.py
│   ├── common.py
│   ├── order.py
│   ├── product.py
│   └── review.py
├── services/
│   ├── category_service.py
│   ├── order_service.py
│   ├── product_service.py
│   └── review_service.py
└── main.py

docs/
├── api_examples.md
└── architecture.md

scripts/
└── seed_db.py
```

## Architecture Overview

Request flow:

`Route -> Service -> Repository -> Database`

- Routes handle HTTP input and output.
- Services hold business rules.
- Repositories hold SQLAlchemy queries.
- Models define database structure.

More detail: [docs/architecture.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/architecture.md)

## Database Design Summary

- `Category` has many `Product`
- `Product` belongs to one `Category`
- `Product` has many `Review`
- `Order` has many `OrderItem`
- `OrderItem` points to both `Order` and `Product`

The backend stores `product_name_snapshot` and `unit_price` in `OrderItem` so old orders stay historically correct even if product data changes later.

## Environment Variables

Copy `.env.example` to `.env`:

```env
PROJECT_NAME="AI Shopping Assistant Backend"
API_V1_PREFIX="/api/v1"
DATABASE_URL="sqlite:///./shopping_assistant.db"
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
```

If your machine uses `python3`:

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

Start the API server:

```bash
uvicorn app.main:app --reload
```

Swagger docs:

- `http://127.0.0.1:8000/docs`

Health endpoints:

- `GET http://127.0.0.1:8000/`
- `GET http://127.0.0.1:8000/api/v1/health`

## Seeding the Database

Run:

```bash
python scripts/seed_db.py
```

Or:

```bash
python3 scripts/seed_db.py
```

Seed behavior:

- adds starter categories, products, and reviews
- skips seeding if data already exists
- does not duplicate rows when run multiple times

The SQLite file appears in the project root as `shopping_assistant.db`.

If you want a fresh local database:

1. Stop the server.
2. Delete `shopping_assistant.db`.
3. Start the server again.
4. Run the seed script again.

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- Curl examples: [docs/api_examples.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/api_examples.md)

## API Endpoints Summary

### Health

- `GET /`
- `GET /api/v1/health`

### Categories

- `POST /api/v1/categories`
- `GET /api/v1/categories`
- `GET /api/v1/categories/{category_id}`
- `PATCH /api/v1/categories/{category_id}`
- `DELETE /api/v1/categories/{category_id}`

### Products

- `POST /api/v1/products`
- `GET /api/v1/products`
- `GET /api/v1/products/search`
- `GET /api/v1/products/with-ratings`
- `GET /api/v1/products/{product_id}`
- `GET /api/v1/products/{product_id}/rating`
- `PATCH /api/v1/products/{product_id}`
- `DELETE /api/v1/products/{product_id}`

### Reviews

- `POST /api/v1/products/{product_id}/reviews`
- `GET /api/v1/products/{product_id}/reviews`
- `GET /api/v1/reviews/{review_id}`
- `PATCH /api/v1/reviews/{review_id}`
- `DELETE /api/v1/reviews/{review_id}`

### Orders

- `POST /api/v1/orders`
- `GET /api/v1/orders`
- `GET /api/v1/orders/{order_id}`
- `PATCH /api/v1/orders/{order_id}/status`

## Curl Examples By Domain

### Health

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/v1/health
```

### Categories

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/categories" \
-H "Content-Type: application/json" \
-d '{
  "name": "Dairy",
  "description": "Organic milk, cheese, yogurt, and dairy products"
}'
```

### Products

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

### Reviews

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products/1/reviews" \
-H "Content-Type: application/json" \
-d '{
  "rating": 5,
  "reviewer_name": "Sazzad",
  "review_text": "Fresh and high quality product."
}'
```

### Ratings

```bash
curl "http://127.0.0.1:8000/api/v1/products/1/rating"
curl "http://127.0.0.1:8000/api/v1/products/with-ratings"
```

### Orders

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

## Error Response Format

HTTP errors now follow a consistent structure:

```json
{
  "success": false,
  "error": {
    "message": "Category not found"
  }
}
```

Validation errors look like:

```json
{
  "success": false,
  "error": {
    "message": "Validation error",
    "details": []
  }
}
```

Unexpected server errors look like:

```json
{
  "success": false,
  "error": {
    "message": "Internal server error"
  }
}
```

## Soft Delete for Products

Deleting a product does not remove the row from the database.  
The backend sets `is_active = false`, which keeps historical order and review relationships intact.

## Why Order Delete Is Intentionally Not Implemented

Orders are business records. In real systems, they are usually cancelled or status-updated instead of deleted.

## Portfolio Talking Points

- clean layered architecture with route, service, repository, and model separation
- SQLAlchemy ORM with relationships and transaction-aware business logic
- Pydantic validation for request and response shapes
- centralized error handling for cleaner API consistency
- Swagger documentation for easy API exploration
- AI-ready backend foundation for a future shopping assistant

## Future Roadmap

- Phase 8 AI agent integration
- optional image search later
- Alembic migrations later
- PostgreSQL later
- authentication later

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
- Category CRUD endpoints
- Product CRUD endpoints
- Review CRUD endpoints
- Rating endpoints
- Order endpoints

## Before Phase 8

Make sure you understand:

- why services hold business rules instead of routes
- why repositories should not raise `HTTPException`
- how centralized exception handlers standardize error payloads
- why only errors are standardized, not all successful responses
- how soft delete differs from hard delete
- why the backend is now a strong foundation for AI features later
