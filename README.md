# AI Shopping Assistant Backend

Portfolio-ready FastAPI backend with a Streamlit frontend for an organic grocery shopping assistant.

Current phase: **Phase 9 - Streamlit Frontend**

## Project Overview

This project now has:

- a FastAPI backend as the source of truth
- a Streamlit frontend for browsing, ordering, and chatting
- a LangChain + Groq AI shopping assistant

The frontend does not access SQLite directly.  
It talks to the FastAPI backend through HTTP requests.

## What The System Does

- browse products with ratings
- search and filter products
- submit product reviews
- add products to a cart
- create orders
- view recent orders
- update order status
- chat with an AI shopping assistant

## Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic and Pydantic Settings
- LangChain
- Groq
- Streamlit
- requests

## Architecture

Backend flow:

`Route -> Service -> Repository -> SQLAlchemy Model -> Database`

Frontend flow:

`Streamlit UI -> frontend/api_client.py -> FastAPI backend`

AI flow:

`Streamlit chat UI -> POST /api/v1/chat -> Agent Service -> LangChain/Groq Agent -> Tools -> Existing Services/Repositories -> Database`

More detail:

- [docs/architecture.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/architecture.md)
- [docs/api_examples.md](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/docs/api_examples.md)

## Why The Frontend Uses HTTP

The Streamlit app is only the frontend.

It does not:

- import backend repositories
- import backend services
- query SQLite directly
- duplicate business logic

This keeps the backend as the source of truth and makes the app easier to scale later.

## Environment Variables

Backend `.env`:

```env
PROJECT_NAME="AI Shopping Assistant Backend"
API_V1_PREFIX="/api/v1"
DATABASE_URL="sqlite:///./shopping_assistant.db"
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="qwen/qwen3-32b"
AI_AGENT_ENABLED=true
```

Frontend optional environment variable:

```env
FASTAPI_BASE_URL=http://127.0.0.1:8000/api/v1
```

If `FASTAPI_BASE_URL` is not set, the frontend uses that default automatically.

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Run The Backend

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Backend URLs:

- API root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Run The Frontend

In another terminal:

```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Frontend URL:

- `http://localhost:8501`

## Streamlit Frontend Pages

### Home

- backend health/status check
- project overview
- quick navigation tips

### Products

- product cards in a grid
- rating display
- simple filters
- add to cart
- view reviews
- submit reviews

### Cart / Order

- customer name and email
- quantity controls
- remove item button
- estimated total
- create order through backend API

### AI Assistant

- chat UI with `st.chat_message`
- chat history in session state
- sends messages to `POST /api/v1/chat`
- backend agent decides whether to search, rate, or checkout

### Orders

- recent orders list
- nested order items
- optional status update UI

## Product Browsing

The frontend loads products from:

- `GET /api/v1/products/with-ratings`

Then Streamlit applies simple display filters for:

- search text
- organic only
- max price
- active products only

This is acceptable for beginner learning and small datasets.  
For larger production datasets, backend-side filtering should be preferred.

## Cart And Order Creation

The cart is stored in `st.session_state.cart`.

When the user places an order, Streamlit sends:

- customer name
- customer email
- product IDs and quantities

to:

- `POST /api/v1/orders`

The backend still calculates the final trusted total and validates stock.

## Review Submission

On the Products page, the user can submit:

- reviewer name
- rating
- review text

The frontend sends that to:

- `POST /api/v1/products/{product_id}/reviews`

## AI Chat

The chat page is pure UI.  
It does not call the order API directly and does not query product data directly.

Instead, it sends chat requests to:

- `POST /api/v1/chat`

The backend agent then uses tools to:

- search products
- get ratings
- create an order through the existing order service

If `GROQ_API_KEY` is missing, the backend returns a friendly error and the rest of the app still works.

## Orders Page

The Orders page uses:

- `GET /api/v1/orders`
- `PATCH /api/v1/orders/{order_id}/status`

It shows:

- order ID
- customer info
- status
- total amount
- created time
- nested items

## Seeding Database

```bash
python scripts/seed_db.py
```

The seed script is safe to run multiple times because it skips seeding if data already exists.

## Troubleshooting

### Backend not running

- start FastAPI with `uvicorn app.main:app --reload`
- verify `http://127.0.0.1:8000/api/v1/health`

### Groq key missing

- set `GROQ_API_KEY` in `.env`
- chat endpoint depends on it, but the rest of the backend does not

### No products showing

- run `python scripts/seed_db.py`
- confirm backend is using the correct SQLite file

### Order fails due to stock

- reduce requested quantity
- check current stock on the Products page

## Portfolio Talking Points

- clean layered backend architecture
- Streamlit frontend separated from backend business logic
- SQLAlchemy ORM for relational data
- Pydantic validation and structured responses
- AI-ready chat layer built on existing backend services
- product reviews, ratings, and order workflows

## Future Roadmap

- image-aware shopping features later
- payment flow later
- authentication later
- Alembic migrations later
- PostgreSQL later

## Existing Endpoints Still Work

- `GET /`
- `GET /api/v1/health`
- Category CRUD
- Product CRUD
- Review CRUD
- Rating endpoints
- Order endpoints
- Chat endpoint

## Before The Next Phase

Make sure you understand:

- why Streamlit stays thin and uses HTTP
- why the backend remains the source of truth
- how `st.session_state` is used for cart and chat memory
- how the AI chat page differs from direct CRUD pages
- how frontend and backend can evolve independently
