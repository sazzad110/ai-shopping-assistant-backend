# Architecture Overview

This backend uses a simple layered architecture to keep the code clear and beginner-friendly.

## Request Flow

`Route -> Service -> Repository -> Database`

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
