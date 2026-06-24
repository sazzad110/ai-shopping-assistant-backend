from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

import app.models
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)


app = FastAPI(
    title="AI Shopping Assistant Backend",
    description="Backend API for an organic grocery shopping assistant",
    version="0.1.0",
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# For beginner learning, we create tables automatically when the app starts.
# In real production projects, database schema changes should be managed with Alembic migrations.
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to AI Shopping Assistant Backend",
        "docs_url": "/docs",
    }


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
