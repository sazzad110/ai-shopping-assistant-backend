# AI Shopping Assistant Backend

Backend API for an organic grocery shopping assistant.

Current phase: **Phase 6 - Order APIs and Backend Business Logic**

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy ORM
- SQLite
- Pydantic Settings
- python-dotenv

## Folder Structure

```text
app/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── router.py
│       └── routes/
│           ├── __init__.py
│           ├── categories.py
│           ├── health.py
│           ├── orders.py
│           ├── products.py
│           └── reviews.py
├── models/
│   ├── __init__.py
│   ├── category.py
│   ├── order.py
│   ├── order_item.py
│   ├── product.py
│   └── review.py
├── repositories/
│   ├── __init__.py
│   ├── category_repository.py
│   ├── order_repository.py
│   ├── product_repository.py
│   └── review_repository.py
├── schemas/
│   ├── __init__.py
│   ├── category.py
│   ├── order.py
│   ├── product.py
│   └── review.py
├── services/
│   ├── __init__.py
│   ├── category_service.py
│   ├── order_service.py
│   ├── product_service.py
│   └── review_service.py
└── core/
    ├── __init__.py
    ├── config.py
    └── database.py

scripts/
└── seed_db.py

requirements.txt
.env.example
README.md
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
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

### 4. Create your environment file

Copy `.env.example` to `.env` and keep the default values.

Example values:

```env
PROJECT_NAME="AI Shopping Assistant Backend"
API_V1_PREFIX="/api/v1"
DATABASE_URL="sqlite:///./shopping_assistant.db"
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

### 6. Seed the database

```bash
python scripts/seed_db.py
```

If your machine uses `python3`, run:

```bash
python3 scripts/seed_db.py
```

## How to Test the API

Open these URLs in your browser or API tool:

- GET [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- GET [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Example `curl` commands:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/v1/health
```

## Phase 6: Order APIs Added

This phase adds order creation and order management with the same clean layers:

- schema layer
- repository layer
- service layer
- route layer

## What Each Layer Means

- Schemas define request and response shapes.
- Routes receive HTTP requests and return HTTP responses.
- Services contain business rules such as duplicate checks and not-found handling.
- Repositories talk directly to the database using SQLAlchemy.

## How Request Data Flows Through the App

For an order request, the flow is:

1. The route receives the HTTP request.
2. The route sends the validated data to the service layer.
3. The service layer applies business rules.
4. The service layer calls the repository layer.
5. The repository layer runs SQLAlchemy queries.
6. The database returns the result back through the same path.

This gives you a clean separation between API logic and database logic.

## Order Endpoints

- `POST /api/v1/orders`
- `GET /api/v1/orders`
- `GET /api/v1/orders/{order_id}`
- `PATCH /api/v1/orders/{order_id}/status`

## What This Phase Teaches

- An order can contain multiple items.
- Product stock is validated before order creation.
- Stock decreases after order creation.
- `line_total` is calculated for each item by the backend.
- `total_amount` is calculated by the backend and never trusted from user input.
- `product_name_snapshot` and `unit_price` are saved at order time.
- Order status can be updated later.

## Why Product Snapshots Are Stored

If a product name or price changes later, old orders should still show what the customer actually bought at that time.

That is why the backend stores:

- `product_name_snapshot`
- `unit_price`

## How Stock Validation Works

Before creating an order, the service checks every requested product:

- the product exists
- the product is active
- the product has enough stock

If one of these checks fails, the order is rejected before anything is committed.

## Why Orders Are Not Deleted

Real systems usually cancel orders or update their status instead of deleting them completely.

That is why this phase adds `PATCH /orders/{order_id}/status` and intentionally does not add `DELETE /orders/{order_id}`.

## Run the Server

```bash
uvicorn app.main:app --reload
```

## Seed the Database

```bash
python scripts/seed_db.py
```

## Test Order APIs

Create order:

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

List orders:

```bash
curl "http://127.0.0.1:8000/api/v1/orders"
```

List orders with pagination:

```bash
curl "http://127.0.0.1:8000/api/v1/orders?limit=10&offset=0"
```

Get order by ID:

```bash
curl "http://127.0.0.1:8000/api/v1/orders/1"
```

Update order status:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/orders/1/status" \
-H "Content-Type: application/json" \
-d '{
  "status": "confirmed"
}'
```

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
- Category CRUD endpoints
- Product CRUD endpoints
- Review CRUD endpoints
- Rating endpoints
- Swagger docs: `http://127.0.0.1:8000/docs`

## SQLite Database File

With the current `DATABASE_URL`, the SQLite database file appears in the project root as:

```text
shopping_assistant.db
```

## How to Reset the Local Database

If you want a fresh database for learning:

1. Stop the FastAPI server.
2. Delete the `shopping_assistant.db` file from the project root.
3. Start the server again:

```bash
uvicorn app.main:app --reload
```

4. Seed the database again if needed:

```bash
python scripts/seed_db.py
```

## What This Phase Sets Up

- Order creation with multiple items
- Backend stock validation and stock reduction
- Backend calculation of `line_total` and `total_amount`
- Order listing and order detail endpoints
- Order status update endpoint
- A simple repository and service flow for order logic
- The existing database models and seed script from earlier phases

## What Still Does Not Exist Yet

- No AI shopping assistant logic yet

AI agent integration starts in Phase 8, after backend quality improvements in Phase 7.

`/docs` and `/api/v1/health` should still work exactly as before.

## Notes Before Phase 7

Before moving to Phase 7, make sure you understand:

- How FastAPI creates and runs an application from `app/main.py`
- How routers help organize endpoints
- How request validation works with Pydantic schemas
- Why the route layer should not query the database directly
- Why the service layer contains business rules such as stock validation
- Why the repository layer is responsible for SQLAlchemy queries
- How `Depends(get_db)` provides a database session to routes
- How stock can be decreased on SQLAlchemy objects before a later commit
- Why order totals should be calculated by the backend, not trusted from the client
