from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

import logging

from sqlalchemy.exc import SQLAlchemyError

# Логирование ошибок
logger = logging.getLogger("uvicorn.error")


async def sqlalchemy_exception_handler(request, exc) -> JSONResponse:
    logger.error(f"SQLAlchemyError:{exc}")
    if "duplicate key value violates unique constraint" in str(exc):
        return JSONResponse(
            status_code=400,
            content={"detail": "Двигатель с таким названием уже существует. Пожалуйста, используйте другое название."}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": f"Server Error(SqlAlchemyError)"},
    )

async def db_connection_exception_handler(request, exc) -> JSONResponse:
    logger.error(f"Database connection failed: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Database connection failed. Please try again later."}
    )

# Обработчик для общих ошибок (Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error occurred."}
    )

# Обработчик для HTTP ошибок (например, 404, 400 и т.д.)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message handler": exc.detail}
    )

# Обработчик для Pydantic ValidationError (например, некорректные данные)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Pydantic Validation Error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Invalid data provided."
        }
    )

# Обработчик для ошибок в запросах (RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request Validation Error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Error in request validation."
        }
    )