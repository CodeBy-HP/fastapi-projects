from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from contextlib import asynccontextmanager
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import settings
from app.core.logger import setup_logger, get_logger, LoggerConfig
from app.core.database import db
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.core.exceptions import (
    validation_exception_handler,
    pydantic_validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
    product_not_found_handler,
    invalid_product_id_handler,
    ProductNotFoundException,
    InvalidProductIdException,
)
from app.routes.product import router as product_router

# Initialize the logger
logger_config = LoggerConfig(
    logger_name="app",
    log_level=settings.LOG_LEVEL,
    log_dir=settings.LOG_DIR,
    log_to_console=settings.LOG_TO_CONSOLE,
    log_to_file=settings.LOG_TO_FILE,
    use_colors=settings.LOG_USE_COLORS,
)
setup_logger(logger_config)

# Get logger instance for this module
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager for startup and shutdown events.
    
    Handles:
    - Database connection on startup
    - Graceful shutdown on application exit
    """
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
        extra={
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        }
    )

    try:
        # Connect to database
        await db.connect_db()
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.critical(
            f"Failed to start application: {str(e)}",
            exc_info=True
        )
        raise

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")
    try:
        await db.close_db()
        logger.info("Application shutdown completed successfully")
    except Exception as e:
        logger.error(
            f"Error during shutdown: {str(e)}",
            exc_info=True
        )


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A production-ready Product Inventory API built with FastAPI",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# === Middlewares ===
# Request logging middleware (should be first to log all requests)
app.add_middleware(RequestLoggingMiddleware)

# Security headers middleware
if settings.ENABLE_SECURITY_HEADERS:
    app.add_middleware(SecurityHeadersMiddleware)
    logger.info("Security headers middleware enabled")

# CORS middleware (should be last in middleware chain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS enabled for origins: {settings.ALLOWED_ORIGINS}")

# === Exception Handlers ===
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ConnectionFailure, database_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ServerSelectionTimeoutError, database_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ProductNotFoundException, product_not_found_handler)  # type: ignore[arg-type]
app.add_exception_handler(InvalidProductIdException, invalid_product_id_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)  # type: ignore[arg-type]

logger.info("Exception handlers registered")

# === Routers ===
app.include_router(product_router)
logger.info("Product router registered")


# === Root endpoint ===
@app.get("/", tags=["Root"], description="Welcome message and API information.")
async def root() -> dict[str, str]:
    """
    Root endpoint returning API information.
    
    Returns:
        dict: API name and version
    """
    logger.debug("Root endpoint accessed")
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": f"{settings.APP_VERSION}",
        "environment": settings.ENVIRONMENT,
    }


# === Health check endpoint ===
@app.get("/health", tags=["Health"], description="Health check endpoint")
async def health_check():
    """
    Health check endpoint to verify application and database status.
    
    Returns:
        dict: Health status information
    """
    logger.debug("Health check endpoint accessed")
    
    # Check database health
    db_healthy = await db.health_check()
    
    overall_status = "healthy" if db_healthy else "unhealthy"
    
    response = {
        "status": overall_status,
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_healthy else "disconnected",
    }
    
    if not db_healthy:
        logger.warning("Health check failed: Database is not healthy")
    
    return response


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting application with uvicorn")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
