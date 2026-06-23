# AI Shopping Assistant Backend

Backend API for an organic grocery shopping assistant.

Current phase: **Phase 4 - Product CRUD with Route, Service, and Repository Layers**

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
│           └── products.py
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
│   └── product_repository.py
├── schemas/
│   ├── __init__.py
│   ├── category.py
│   └── product.py
├── services/
│   ├── __init__.py
│   ├── category_service.py
│   └── product_service.py
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

## Phase 4: Product CRUD Added

This phase adds full Product CRUD with the same clean layers:

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

For a product request, the flow is:

1. The route receives the HTTP request.
2. The route sends the validated data to the service layer.
3. The service layer applies business rules.
4. The service layer calls the repository layer.
5. The repository layer runs SQLAlchemy queries.
6. The database returns the result back through the same path.

This gives you a clean separation between API logic and database logic.

## Product Endpoints

- `POST /api/v1/products`
- `GET /api/v1/products`
- `GET /api/v1/products/search`
- `GET /api/v1/products/{product_id}`
- `PATCH /api/v1/products/{product_id}`
- `DELETE /api/v1/products/{product_id}`

## How Product CRUD Works

- Products belong to categories.
- The service layer validates that `category_id` exists before create or category change.
- Product delete is a soft delete, which means the row stays in the database and `is_active` becomes `false`.
- Product list supports simple filters and pagination.
- Product search supports searching by name and description.

## How Category Validation Works

Before creating a product, the service checks that the category exists.

Before updating `category_id`, the service checks that the new category exists.

If the category does not exist, the API returns:

```text
404 Not Found
Category not found
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

## Seed the Database

```bash
python scripts/seed_db.py
```

## Test Product CRUD

Create product:

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

List products:

```bash
curl "http://127.0.0.1:8000/api/v1/products"
```

List active products only:

```bash
curl "http://127.0.0.1:8000/api/v1/products?is_active=true"
```

Filter by category:

```bash
curl "http://127.0.0.1:8000/api/v1/products?category_id=1"
```

Filter organic products:

```bash
curl "http://127.0.0.1:8000/api/v1/products?is_organic=true"
```

Filter by max price:

```bash
curl "http://127.0.0.1:8000/api/v1/products?max_price=10"
```

Pagination:

```bash
curl "http://127.0.0.1:8000/api/v1/products?limit=5&offset=0"
```

Search products:

```bash
curl "http://127.0.0.1:8000/api/v1/products/search?query=honey"
```

Get product by ID:

```bash
curl "http://127.0.0.1:8000/api/v1/products/1"
```

Update product:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/products/1" \
-H "Content-Type: application/json" \
-d '{
  "price": 7.49,
  "stock_quantity": 40
}'
```

Soft delete product:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/products/1"
```

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
- Category CRUD endpoints
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

- Product CRUD endpoints
- Pydantic request and response schemas for products
- A simple repository layer for product database access
- A simple service layer for product business rules
- Product filters and simple product search
- The existing database models and seed script from earlier phases

## What Still Does Not Exist Yet

- No Review CRUD yet
- No Order APIs yet
- No AI shopping assistant logic yet

Product ratings are not implemented yet. Review CRUD and ratings start in Phase 5.

`/docs` and `/api/v1/health` should still work exactly as before.

## Notes Before Phase 5

Before moving to Phase 5, make sure you understand:

- How FastAPI creates and runs an application from `app/main.py`
- How routers help organize endpoints
- How request validation works with Pydantic schemas
- Why the route layer should not query the database directly
- Why the service layer handles business rules like category validation
- Why the repository layer is responsible for SQLAlchemy queries
- How `Depends(get_db)` provides a database session to routes
- Why soft delete keeps product rows available for later business rules
- How filters and pagination shape list results
