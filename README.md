# AI Shopping Assistant Backend

Backend API for an organic grocery shopping assistant.

Current phase: **Phase 5 - Review CRUD and Product Rating Aggregation**

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
│   ├── product_repository.py
│   └── review_repository.py
├── schemas/
│   ├── __init__.py
│   ├── category.py
│   ├── product.py
│   └── review.py
├── services/
│   ├── __init__.py
│   ├── category_service.py
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

## Phase 5: Review CRUD and Ratings Added

This phase adds review management and product rating aggregation with the same clean layers:

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

For a review request, the flow is:

1. The route receives the HTTP request.
2. The route sends the validated data to the service layer.
3. The service layer applies business rules.
4. The service layer calls the repository layer.
5. The repository layer runs SQLAlchemy queries.
6. The database returns the result back through the same path.

This gives you a clean separation between API logic and database logic.

## Review Endpoints

- `POST /api/v1/products/{product_id}/reviews`
- `GET /api/v1/products/{product_id}/reviews`
- `GET /api/v1/reviews/{review_id}`
- `PATCH /api/v1/reviews/{review_id}`
- `DELETE /api/v1/reviews/{review_id}`

## Rating Endpoints

- `GET /api/v1/products/{product_id}/rating`
- `GET /api/v1/products/with-ratings`

## How Review and Rating Logic Works

- Reviews belong to products.
- Rating validation is handled by Pydantic and must stay between `1` and `5`.
- Average rating is calculated from review rows when needed.
- Average rating is not stored directly on the product table in this phase.

## Why Calculated Ratings Are Useful

For beginner learning, calculated ratings are simpler and safer than storing duplicate rating data on the `products` table.

This avoids keeping two sources of truth in sync every time a review is created, updated, or deleted.

## How Product Existence Validation Works

Before creating a review, listing reviews, or calculating rating for a product, the service checks that the product exists.

If the product does not exist, the API returns:

```text
404 Not Found
Product not found
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

## Seed the Database

```bash
python scripts/seed_db.py
```

## Test Review CRUD and Rating Endpoints

Create review:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products/1/reviews" \
-H "Content-Type: application/json" \
-d '{
  "rating": 5,
  "reviewer_name": "Sazzad",
  "review_text": "Fresh and high quality product."
}'
```

List reviews for product:

```bash
curl "http://127.0.0.1:8000/api/v1/products/1/reviews"
```

Get one review:

```bash
curl "http://127.0.0.1:8000/api/v1/reviews/1"
```

Update review:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/reviews/1" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4,
  "review_text": "Still good, but delivery was a little late."
}'
```

Delete review:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/reviews/1"
```

Get product rating:

```bash
curl "http://127.0.0.1:8000/api/v1/products/1/rating"
```

Get products with ratings:

```bash
curl "http://127.0.0.1:8000/api/v1/products/with-ratings"
```

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
- Category CRUD endpoints
- Product CRUD endpoints
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

- Review CRUD endpoints
- Rating validation using Pydantic
- Product rating summary endpoint
- Product list endpoint with calculated ratings
- A simple repository and service flow for review logic
- The existing database models and seed script from earlier phases

## What Still Does Not Exist Yet

- No Order APIs yet
- No AI shopping assistant logic yet

Order APIs start in Phase 6.

`/docs` and `/api/v1/health` should still work exactly as before.

## Notes Before Phase 6

Before moving to Phase 6, make sure you understand:

- How FastAPI creates and runs an application from `app/main.py`
- How routers help organize endpoints
- How request validation works with Pydantic schemas
- Why the route layer should not query the database directly
- Why the service layer validates product existence before review operations
- Why the repository layer is responsible for SQLAlchemy queries
- How `Depends(get_db)` provides a database session to routes
- How `func.avg` and `func.count` are used to calculate rating data
- Why calculated rating values avoid storing duplicate data too early
