"""
Custom Exception Handlers for Production-Ready FastAPI Application

This module provides centralized exception handling with proper logging
and user-friendly error responses.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.logger import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle FastAPI validation errors with detailed logging.
    
    Args:
        request: The incoming request
        exc: The validation exception
        
    Returns:
        JSONResponse with validation error details
    """
    errors = exc.errors()
    
    logger.warning(
        f"Validation error on {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "errors": errors,
            "client_host": request.client.host if request.client else "unknown",
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validation error occurred",
            "errors": errors,
        },
    )


async def pydantic_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: The incoming request
        exc: The Pydantic validation exception
        
    Returns:
        JSONResponse with validation error details
    """
    errors = exc.errors()
    
    logger.warning(
        f"Pydantic validation error on {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "errors": errors,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Data validation error",
            "errors": errors,
        },
    )


async def database_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Handle database-related exceptions.
    
    Args:
        request: The incoming request
        exc: The database exception
        
    Returns:
        JSONResponse with appropriate error message
    """
    logger.error(
        f"Database error on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
        extra={
            "method": request.method,
            "path": request.url.path,
            "error_type": type(exc).__name__,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "error",
            "message": "Database service temporarily unavailable. Please try again later.",
        },
    )


async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions.
    
    Args:
        request: The incoming request
        exc: The exception
        
    Returns:
        JSONResponse with generic error message
    """
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
        extra={
            "method": request.method,
            "path": request.url.path,
            "error_type": type(exc).__name__,
            "client_host": request.client.host if request.client else "unknown",
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


# Custom application exceptions
class ProductNotFoundException(Exception):
    """Raised when a product is not found in the database."""
    
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class InvalidProductIdException(Exception):
    """Raised when an invalid product ID format is provided."""
    
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Invalid product ID format: {product_id}")


async def product_not_found_handler(
    request: Request, exc: ProductNotFoundException
) -> JSONResponse:
    """Handle ProductNotFoundException."""
    logger.info(
        f"Product not found: {exc.product_id} on {request.method} {request.url.path}",
        extra={
            "product_id": exc.product_id,
            "path": request.url.path,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": "error",
            "message": str(exc),
            "product_id": exc.product_id,
        },
    )


async def invalid_product_id_handler(
    request: Request, exc: InvalidProductIdException
) -> JSONResponse:
    """Handle InvalidProductIdException."""
    logger.warning(
        f"Invalid product ID: {exc.product_id} on {request.method} {request.url.path}",
        extra={
            "product_id": exc.product_id,
            "path": request.url.path,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": str(exc),
            "product_id": exc.product_id,
        },
    )
