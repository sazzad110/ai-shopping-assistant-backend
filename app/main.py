from fastapi import FastAPI

import app.models
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine


app = FastAPI(
    title="AI Shopping Assistant Backend",
    description="Backend API for an organic grocery shopping assistant",
    version="0.1.0",
)

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
