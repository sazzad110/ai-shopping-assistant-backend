# Architecture Overview

This backend uses a simple layered architecture to keep the code clear and beginner-friendly.

## Request Flow

`Route -> Service -> Repository -> Database`

## AI Flow

`Chat Route -> Agent Service -> LangChain Agent -> Tools -> Existing Services/Repositories -> Database`

## Frontend Flow

`Streamlit UI -> frontend/api_client.py -> FastAPI routes -> services -> repositories -> SQLAlchemy models -> SQLite database`

## Layer Responsibilities

### Route layer

- Receives HTTP requests
- Reads path params, query params, and request bodies
- Uses `Depends(get_db)` to get a database session
- Calls the service layer

### Service layer

- Holds business rules
- Validates things like duplicate names, stock, and product existence
- Decides when to raise `HTTPException`
- Keeps route files thin

### Agent layer

- Adds conversational behavior on top of the existing backend
- Uses LangChain tools
- Reuses existing business logic instead of replacing CRUD
- Does not connect to SQLite manually

### Frontend layer

- Displays product browsing, cart, orders, and chat pages
- Talks to FastAPI only through HTTP requests
- Does not import backend repositories or services
- Does not access SQLite directly

### Repository layer

- Talks directly to SQLAlchemy
- Runs queries, inserts, updates, and deletes
- Does not raise `HTTPException`

### Model layer

- Defines database tables using SQLAlchemy ORM
- Describes relationships between categories, products, reviews, orders, and order items

## Why This Structure Helps

- Easier to test and maintain
- Business logic is not mixed with HTTP code
- SQLAlchemy queries stay in one place
- The project is easier to explain in a portfolio or interview
- AI tools do not replace CRUD; they reuse CRUD and service logic
- The frontend stays thin because the backend remains the source of truth
