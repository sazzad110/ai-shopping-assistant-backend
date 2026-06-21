# AI Shopping Assistant Backend

Backend API for an organic grocery shopping assistant.

Current phase: **Phase 2 - SQLAlchemy Models and Database Setup**

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
│           └── health.py
├── models/
│   ├── __init__.py
│   ├── category.py
│   ├── order.py
│   ├── order_item.py
│   ├── product.py
│   └── review.py
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

## Phase 2: Models Added

This phase adds these SQLAlchemy models:

- `Category`
- `Product`
- `Review`
- `Order`
- `OrderItem`

## Beginner-Friendly Relationship Overview

- One category can have many products.
- One product belongs to one category.
- One product can have many reviews.
- One order can have many order items.
- One order item belongs to one order.
- One order item belongs to one product.

These relationships are defined with SQLAlchemy `relationship()` and `back_populates` so both sides stay connected in Python code.

## How Tables Are Created Automatically

When you start the FastAPI app with:

```bash
uvicorn app.main:app --reload
```

the app imports the models and runs:

```python
Base.metadata.create_all(bind=engine)
```

This creates the SQLite tables if they do not already exist.

This is helpful for beginner learning. In real projects, database changes should usually be handled with Alembic migrations instead.

## Seeding Sample Data

After the tables are created, run:

```bash
python scripts/seed_db.py
```

This script:

- checks whether categories already exist
- avoids inserting duplicate starter data
- adds sample categories
- adds sample products
- adds a few sample reviews

## Where the SQLite Database File Appears

With the current `DATABASE_URL`, the SQLite file will appear in the project root as:

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

- SQLAlchemy models for categories, products, reviews, orders, and order items
- Automatic table creation for beginner learning
- A simple seed script for local development data
- The same working FastAPI routes from Phase 1

## What Still Does Not Exist Yet

- No CRUD endpoints yet
- No Pydantic schemas yet
- No repositories or services yet
- No AI shopping assistant logic yet

The database exists now, but you still cannot create or list products through the API until later phases.

`/docs` and `/api/v1/health` should still work exactly as before.

## Notes Before Phase 3

Before moving to Phase 3, make sure you understand:

- How FastAPI creates and runs an application from `app/main.py`
- How routers help organize endpoints
- How settings are loaded from `app/core/config.py`
- How SQLAlchemy models map Python classes to database tables
- The difference between `engine`, `SessionLocal`, and `Base`
- How foreign keys connect tables together
- How `relationship()` and `back_populates` help navigate related data
- Why `create_all()` is acceptable for learning but not the long-term production approach
