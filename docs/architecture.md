# Architecture Overview

This project uses a layered FastAPI backend, a Streamlit frontend, and an AI shopping assistant built with LangChain and Groq.

The key design idea is simple:

- the backend remains the source of truth
- the frontend stays thin
- the AI assistant reuses backend business logic through tools

## High-Level System View

### Standard API Flow

`Client -> FastAPI Route -> Service -> Repository -> SQLAlchemy Model -> Database`

This is the normal flow for:

- categories
- products
- reviews
- ratings
- orders

### Frontend Flow

`Streamlit UI -> frontend/api_client.py -> FastAPI endpoints`

The Streamlit app only talks to the backend over HTTP. It does not access SQLite directly and does not import repository code.

### AI Assistant Flow

`Streamlit Chat UI`
-> `frontend/api_client.py::chat_with_agent(...)`
-> `POST /api/v1/chat`
-> `app/api/v1/routes/chat.py`
-> `app/services/agent_service.py`
-> `app/agent/shopping_agent.py`
-> `LangChain/Groq model + tools`
-> `existing services/repositories`
-> `database`
-> assistant reply

## Layer Responsibilities

### Route Layer

Files:

- `app/api/v1/routes/chat.py`
- `app/api/v1/routes/orders.py`
- `app/api/v1/routes/products.py`
- `app/api/v1/routes/reviews.py`
- `app/api/v1/routes/categories.py`
- `app/api/v1/routes/health.py`

Responsibilities:

- receive HTTP requests
- validate request shape through Pydantic schemas
- get a DB session with `Depends(get_db)`
- call the service layer
- return structured API responses

Routes stay intentionally thin. They should not contain business logic or direct SQL queries.

### Service Layer

Files:

- `app/services/agent_service.py`
- `app/services/order_service.py`
- `app/services/product_service.py`
- `app/services/review_service.py`
- `app/services/category_service.py`

Responsibilities:

- coordinate business rules
- validate domain behavior
- raise `HTTPException` when needed
- keep route handlers simple

Examples:

- `order_service.create_order(...)` validates stock and calculates totals
- `review_service.get_product_rating(...)` validates the product before returning rating data
- `agent_service.chat_with_agent(...)` bridges FastAPI and the AI agent

### Repository Layer

Files:

- `app/repositories/product_repository.py`
- `app/repositories/order_repository.py`
- `app/repositories/review_repository.py`
- `app/repositories/category_repository.py`

Responsibilities:

- execute SQLAlchemy queries
- load, create, and update database records
- avoid HTTP-specific behavior

Repositories should not decide API responses. They focus on data access.

### Model Layer

Files in `app/models/`

Responsibilities:

- define database tables
- define relationships between entities
- represent persisted data with SQLAlchemy ORM

Core entities include:

- category
- product
- review
- order
- order item

### Frontend Layer

Files:

- `frontend/streamlit_app.py`
- `frontend/api_client.py`
- `frontend/ui_helpers.py`

Responsibilities:

- render the UI
- store temporary frontend state in `st.session_state`
- send HTTP requests to FastAPI
- display results and errors

Important limitation by design:

- the frontend does not access the database directly
- the frontend does not run business logic
- the frontend does not interpret chat intent into order creation itself

## AI Assistant Architecture

The AI assistant is the most distinctive part of the project.

It is not a separate database system and not a shortcut around the backend. It is a reasoning layer on top of existing backend logic.

### Main AI Files

- `app/api/v1/routes/chat.py`
- `app/schemas/chat.py`
- `app/services/agent_service.py`
- `app/agent/shopping_agent.py`
- `app/agent/tools.py`
- `app/agent/prompts.py`
- `app/core/config.py`

### Chat Request Flow

When the user sends a message from Streamlit:

1. `frontend/streamlit_app.py` reads the new input
2. it stores the new message in `st.session_state.chat_messages`
3. it sends:
   - `message`: latest user message
   - `history`: previous messages only
   - optional `customer_name`
   - optional `customer_email`
4. FastAPI validates this data with `ChatRequest`
5. the route passes the request to `agent_service.chat_with_agent(...)`
6. the service calls `run_shopping_agent(...)`
7. the agent may call tools
8. the final reply is returned as `ChatResponse`

### Why History Comes From the Frontend

This project currently keeps chat memory in Streamlit session state, not in the backend database.

That means the frontend must resend prior messages on every chat request.

This enables follow-up reasoning such as:

- "show me organic honey under $10"
- "order the first product"

The agent can understand the second message because it sees the earlier assistant reply that included product IDs.

### How the Agent Is Created

Inside `app/agent/shopping_agent.py`, the agent is created per request.

Why this is a good design:

- tools need the current SQLAlchemy session
- missing `GROQ_API_KEY` should affect only the chat endpoint
- app startup should still work even if AI is disabled or misconfigured

### How Tool Calling Works

`create_shopping_tools(db)` creates three tools:

- `search_products`
- `get_rating`
- `checkout`

The agent reads the system prompt, decides which tool to call, receives tool results, and then continues reasoning.

Example:

`User -> "I want organic honey under $10 with rating 4"`

Likely flow:

1. agent calls `search_products(query="honey", max_price=10, is_organic=True)`
2. tool uses `product_repository.search_products(...)`
3. agent checks ratings with `get_rating(product_id=...)`
4. tool uses `review_service.get_product_rating(...)`
5. agent replies with matching products and includes `(ID: X)`

### Why the Agent Uses Tools Instead of Direct DB Access

This keeps the AI layer safe and maintainable.

Benefits:

- no duplicated order logic
- no raw `sqlite3` access inside tools
- stock validation remains in `order_service`
- data access remains in repositories
- backend remains consistent across chat and non-chat flows

## Chat Ordering vs Cart Ordering

There are two order flows in this project.

### Cart Order Flow

`Streamlit Cart UI -> frontend/api_client.py -> POST /api/v1/orders -> order_service -> repository -> database`

Used when the user manually adds items to cart and clicks place order.

### Chat Agent Order Flow

`Streamlit Chat UI -> POST /api/v1/chat -> AI agent -> checkout tool -> order_service -> repository -> database`

Used when the user wants to order through conversation.

Important difference:

- cart flow is directly user-driven through form data
- chat flow is reasoning-driven and must respect agent prompt rules

## Why This Structure Works Well

- clean separation between UI, HTTP, business logic, and data access
- AI assistant is integrated without bypassing the backend
- the same service layer is reused in both normal and conversational flows
- easy to explain in interviews and portfolio reviews
- easy to extend later with persistent memory, auth, or external databases
