# AI Shopping Assistant

An AI-first shopping assistant for an organic grocery store, built with FastAPI, Streamlit, SQLAlchemy, LangChain, and Groq.

This project combines a traditional e-commerce backend with a conversational AI assistant that can:

- recommend products from live backend data
- check ratings before suggesting items
- understand follow-up messages like "order the first product"
- create orders through backend business logic instead of bypassing it

The strongest part of this project is the AI assistant architecture:

`Streamlit Chat UI -> FastAPI /api/v1/chat -> LangChain/Groq Agent -> Tools -> Existing Services -> Repositories -> Database`

## Why This Project Stands Out

Most demo chat apps stop at conversation. This one connects an LLM to real application logic.

The assistant does not invent product data and does not write directly to the database. It uses backend tools that call the same service layer used by the normal API. That means the AI flow stays aligned with the rest of the system:

- product search comes from repository-backed data
- rating checks come from the review service
- order creation goes through stock validation and order business rules
- the backend remains the source of truth

## Core Features

### AI Assistant

- natural-language product discovery
- filter-aware recommendations such as organic preference and max price
- rating-aware suggestions using review data
- follow-up chat context using prior message history
- chat-driven checkout through agent tools
- safe ordering rules that require confirmation before purchase

### Shopping Features

- browse products with ratings
- submit reviews
- add products to a cart
- place direct orders from the cart
- view recent orders
- update order status

## Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Pydantic Settings
- LangChain
- Groq
- Streamlit
- requests

## Architecture

### Standard Backend Flow

`Route -> Service -> Repository -> SQLAlchemy Model -> Database`

This is used for products, reviews, ratings, orders, and related CRUD operations.

### Frontend Flow

`Streamlit UI -> frontend/api_client.py -> FastAPI API`

The Streamlit app is a real frontend. It does not import repositories, query SQLite directly, or duplicate backend logic.

### AI Assistant Flow

`User Message`
-> `frontend/streamlit_app.py`
-> `frontend/api_client.py::chat_with_agent(...)`
-> `POST /api/v1/chat`
-> `app/api/v1/routes/chat.py`
-> `app/services/agent_service.py`
-> `app/agent/shopping_agent.py`
-> `app/agent/tools.py`
-> existing services and repositories
-> database
-> assistant reply returned to Streamlit

## AI Assistant Deep Dive

This project is designed so the AI assistant is useful, not just flashy.

### How Chat Works

The Streamlit frontend stores conversation history in `st.session_state.chat_messages`.

Each time the user sends a new message:

1. Streamlit sends the latest message as `message`
2. Streamlit sends earlier messages as `history`
3. FastAPI validates the request with `ChatRequest`
4. `agent_service.chat_with_agent(...)` forwards the request to the LangChain agent
5. the agent reads the system prompt and decides whether to call tools
6. tool results are fed back into the model
7. the final reply is returned to the frontend and stored in session state

### Why the Agent Is Cleanly Integrated

The assistant does not create orders directly from the frontend and does not parse database details on the client side.

Instead:

- Streamlit handles UI and temporary chat memory
- FastAPI handles request validation
- LangChain handles reasoning and tool selection
- tools act as adapters to backend logic
- services enforce business rules
- repositories handle database access

### Tools Used By the Agent

Defined in [app/agent/tools.py](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/app/agent/tools.py):

- `search_products`
- `get_rating`
- `checkout`

These tools are created per request using the current SQLAlchemy session. This is important because:

- tools need the active DB session
- missing Groq configuration should not break the full app at startup
- chat stays isolated from app bootstrapping concerns

### Example AI Flow

User:

`I want organic honey under $10 with rating 4`

Typical agent behavior:

1. reads the system prompt from [app/agent/prompts.py](/Users/sazzad/personal-projects/ai-shopping-assistant-backend/app/agent/prompts.py)
2. calls `search_products(query="honey", max_price=10, is_organic=True)`
3. gets matching products from the database
4. calls `get_rating(product_id=...)` for relevant matches
5. filters out weak matches
6. replies with a numbered list including product IDs like `(ID: 5)`

Follow-up user message:

`I want to order the first product`

Because the frontend sends previous conversation history, the agent can look at its earlier reply, see which product was listed first, recover the correct product ID, and continue the order flow safely.

It will still ask for missing details or confirmation before calling `checkout`.

## Project Structure

```text
app/
  agent/
    prompts.py
    shopping_agent.py
    tools.py
  api/v1/routes/
    chat.py
    orders.py
    products.py
    reviews.py
    categories.py
    health.py
  core/
    config.py
    database.py
    exceptions.py
  models/
  repositories/
  schemas/
  services/

frontend/
  api_client.py
  streamlit_app.py
  ui_helpers.py

scripts/
  seed_db.py
```

## Frontend Pages

### Home

- project overview
- backend health checks
- quick navigation guidance

### Products

- browse products in a grid
- view prices, stock, and ratings
- open reviews
- submit new reviews
- add items to cart

### Cart / Order

- manage cart state in Streamlit session state
- collect customer name and email
- place order through `POST /api/v1/orders`

### AI Assistant

- chat UI using `st.chat_message`
- sends `message + history` to `POST /api/v1/chat`
- displays AI-generated product recommendations
- supports conversational ordering through tools

### Orders

- list recent orders
- inspect nested order items
- update order status

## API Highlights

### Chat Endpoint

`POST /api/v1/chat`

Purpose:

- receive a user message
- receive prior chat history
- run the LangChain/Groq shopping agent
- return the final assistant reply

### Order Endpoint

`POST /api/v1/orders`

Purpose:

- create standard non-chat orders from the cart UI
- validate product availability
- validate stock
- calculate trusted totals on the backend

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

If `FASTAPI_BASE_URL` is not set, the frontend falls back to the local development default.

## Local Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the database

```bash
python scripts/seed_db.py
```

### 4. Run the backend

```bash
uvicorn app.main:app --reload
```

Backend URLs:

- API root: `http://127.0.0.1:8000/`
- health: `http://127.0.0.1:8000/api/v1/health`
- docs: `http://127.0.0.1:8000/docs`

### 5. Run the frontend

In another terminal:

```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Frontend URL:

- `http://localhost:8501`
## Troubleshooting

### Chat endpoint fails

- confirm `GROQ_API_KEY` is set in `.env`
- confirm `AI_AGENT_ENABLED=true`
- verify backend is running at `http://127.0.0.1:8000`

### No products appear

- run `python scripts/seed_db.py`
- confirm the backend is using the expected SQLite database

### Order fails

- verify the product is active
- verify requested quantity is in stock

### Backend unavailable from Streamlit

- check `FASTAPI_BASE_URL`
- confirm `uvicorn app.main:app --reload` is running

## Documentation

- [Architecture Notes](docs/architecture.md)
- [API Examples](docs/api_examples.md)

## Future Improvements

- persistent chat memory
- authentication and user accounts
- PostgreSQL deployment
- Alembic migrations
- image-aware product search
- payment integration
