from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # This handler standardizes errors raised intentionally in the app,
    # such as not found, duplicate data, or bad request errors.
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.detail,
            },
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    # This handler standardizes request validation errors from FastAPI/Pydantic,
    # such as missing fields or invalid types.
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "message": "Validation error",
                "details": exc.errors(),
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # This handler catches unexpected server errors and avoids exposing
    # internal Python tracebacks to API clients.
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": "Internal server error",
            },
        },
    )
