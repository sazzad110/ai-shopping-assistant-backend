# AI Shopping Assistant Backend

Portfolio-ready FastAPI backend for an organic grocery shopping assistant.  
This project now includes a LangChain + Groq conversational shopping agent layered on top of a clean CRUD backend.

Current phase: **Phase 8 - LangChain + Groq AI Shopping Agent**

## What This Backend Does

- manages categories
- manages products with filters, search, ratings, and soft delete
- manages reviews and rating aggregation
- manages orders with stock validation
- exposes a conversational AI shopping assistant at `POST /api/v1/chat`
- keeps the CRUD backend as the source of truth

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy ORM
- SQLite
- Pydantic and Pydantic Settings
- LangChain
- Groq via `langchain-groq`
- python-dotenv

## Features Completed So Far

- FastAPI foundation
- SQLAlchemy models and local database setup
- Category CRUD
- Product CRUD, search, and soft delete
- Review CRUD
- Product rating aggregation
- Order APIs with stock validation
- centralized error handling
- reusable response schemas
- LangChain tool-based chat assistant

## AI Agent Overview

The AI shopping assistant is available at:

- `POST /api/v1/chat`

The agent:

- uses LangChain tools
- uses Groq as the LLM provider
- reuses existing SQLAlchemy session and backend services
- does not query SQLite manually
- does not replace CRUD logic

Image matching is intentionally not included yet.  
No Streamlit frontend is included in this phase.

## Architecture Overview

CRUD flow:

`Route -> Service -> Repository -> SQLAlchemy Model -> Database`

AI flow:

`Chat Route -> Agent Service -> LangChain Agent -> Tools -> Existing Services/Repositories -> Database`

The AI tools reuse the existing backend logic. They do not create their own database connection and do not bypass the application's business rules.

More detail:

- [docs/architecture.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/architecture.md)
- [docs/api_examples.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/api_examples.md)

## Environment Variables

Copy `.env.example` to `.env`:

```env
PROJECT_NAME="AI Shopping Assistant Backend"
API_V1_PREFIX="/api/v1"
DATABASE_URL="sqlite:///./shopping_assistant.db"
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="qwen/qwen3-32b"
AI_AGENT_ENABLED=true
```

Important:

- `GROQ_API_KEY` is required only for `/api/v1/chat`
- the rest of the backend still works without Groq
- if the key is missing, the chat endpoint returns a clean error

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
```

Or:

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

```bash
uvicorn app.main:app --reload
```

Swagger docs:

- `http://127.0.0.1:8000/docs`

Core health endpoints:

- `GET http://127.0.0.1:8000/`
- `GET http://127.0.0.1:8000/api/v1/health`

## Seeding the Database

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
- does not duplicate seed rows

The SQLite file appears in the project root as `shopping_assistant.db`.

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- More curl examples: [docs/api_examples.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/api_examples.md)

## API Endpoints Summary

### Health

- `GET /`
- `GET /api/v1/health`

### Chat

- `POST /api/v1/chat`

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

### Chat

Basic product search:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I want organic honey under $20 with 4.5+ rating"
}'
```

Ask to buy without enough detail:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I want to buy honey"
}'
```

Order with explicit confirmation and customer details:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "I confirm I want to order product ID 1 quantity 2",
  "customer_name": "Sazzad Hasan",
  "customer_email": "sazzad@example.com"
}'
```

Chat with history:

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

### Categories, Products, Reviews, Ratings, Orders

See:

- [docs/api_examples.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/api_examples.md)

## How the AI Tools Work

### `search_products`

- searches existing products by name and description
- uses the existing SQLAlchemy session
- returns only active products
- supports organic and max-price filtering

### `get_rating`

- uses the existing rating logic
- returns product rating summary as JSON text

### `checkout`

- uses the existing order service
- creates a one-item order
- respects existing stock validation and order logic
- returns a friendly success or error message

## Why the Agent Uses Services and Repositories

The AI layer is only a conversational layer.  
The existing backend logic remains the source of truth.

That means the tools:

- do not open raw SQLite connections
- do not run manual SQL outside SQLAlchemy
- do not bypass order, stock, or rating logic

## Error Response Format

Application errors follow a consistent structure:

```json
{
  "success": false,
  "error": {
    "message": "Product not found"
  }
}
```

Validation errors:

```json
{
  "success": false,
  "error": {
    "message": "Validation error",
    "details": []
  }
}
```

## Soft Delete for Products

Deleting a product marks `is_active = false` instead of removing the row.

## Why Order Delete Is Not Implemented

Orders are business records, so status updates are safer than hard deletes.

## Portfolio Talking Points

- clean layered architecture
- SQLAlchemy ORM and relational backend design
- Pydantic validation
- business logic in services
- centralized error handling
- Swagger docs for exploration
- AI-ready backend foundation
- LangChain tools reusing backend logic instead of bypassing it

## Future Roadmap

- Phase 9 or later image-aware shopping improvements
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

## Before The Next Phase

Make sure you understand:

- how the AI agent sits on top of the CRUD backend
- why the agent is not the source of truth
- why the agent is created per request instead of globally
- how tool-calling lets the LLM use existing backend functionality
- why missing `GROQ_API_KEY` should only affect chat, not the whole app
