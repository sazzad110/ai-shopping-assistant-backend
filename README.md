# AI Shopping Assistant Backend

Backend API for an organic grocery shopping assistant.

Current phase: **Phase 3 - Category CRUD with Route, Service, and Repository Layers**

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
│           └── health.py
├── models/
│   ├── __init__.py
│   ├── category.py
│   ├── order.py
│   ├── order_item.py
│   ├── product.py
│   └── review.py
├── repositories/
│   ├── __init__.py
│   └── category_repository.py
├── schemas/
│   ├── __init__.py
│   └── category.py
├── services/
│   ├── __init__.py
│   └── category_service.py
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

## Phase 3: Category CRUD Added

This phase adds full Category CRUD with these layers:

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

For a category request, the flow is:

1. The route receives the HTTP request.
2. The route sends the validated data to the service layer.
3. The service layer applies business rules.
4. The service layer calls the repository layer.
5. The repository layer runs SQLAlchemy queries.
6. The database returns the result back through the same path.

This gives you a clean separation between API logic and database logic.

## Category Endpoints

- `POST /api/v1/categories`
- `GET /api/v1/categories`
- `GET /api/v1/categories/{category_id}`
- `PATCH /api/v1/categories/{category_id}`
- `DELETE /api/v1/categories/{category_id}`

## How Duplicate Category Handling Works

Before creating a category, the service checks whether the same category name already exists.

Before renaming a category, the service checks whether the new name already belongs to another category.

If a duplicate is found, the API returns:

```text
400 Bad Request
Category with this name already exists
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

## Seed the Database

```bash
python scripts/seed_db.py
```

## Test Category CRUD

Create category:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/categories" \
-H "Content-Type: application/json" \
-d '{
  "name": "Dairy",
  "description": "Organic milk, cheese, yogurt, and dairy products"
}'
```

List categories:

```bash
curl "http://127.0.0.1:8000/api/v1/categories"
```

List categories with pagination:

```bash
curl "http://127.0.0.1:8000/api/v1/categories?limit=10&offset=0"
```

Get category by ID:

```bash
curl "http://127.0.0.1:8000/api/v1/categories/1"
```

Update category:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/categories/1" \
-H "Content-Type: application/json" \
-d '{
  "description": "Updated organic dairy products"
}'
```

Delete category:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/categories/1"
```

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
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

- Category CRUD endpoints
- Pydantic request and response schemas for categories
- A simple repository layer for database access
- A simple service layer for business rules
- The existing database models and seed script from earlier phases

## What Still Does Not Exist Yet

- No Product CRUD yet
- No Review CRUD yet
- No Order APIs yet
- No AI shopping assistant logic yet

Product CRUD starts in Phase 4.

`/docs` and `/api/v1/health` should still work exactly as before.

## Notes Before Phase 4

Before moving to Phase 4, make sure you understand:

- How FastAPI creates and runs an application from `app/main.py`
- How routers help organize endpoints
- How request validation works with Pydantic schemas
- Why the route layer should not query the database directly
- Why the service layer handles business rules like duplicate checks
- Why the repository layer is responsible for SQLAlchemy queries
- How `Depends(get_db)` provides a database session to routes
