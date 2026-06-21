from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title="AI Shopping Assistant Backend",
    description="Backend API for an organic grocery shopping assistant",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to AI Shopping Assistant Backend",
        "docs_url": "/docs",
    }


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
