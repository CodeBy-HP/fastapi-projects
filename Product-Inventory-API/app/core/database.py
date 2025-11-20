import asyncio
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import settings
from app.core.logger import get_logger
from app.models.product import Product

logger = get_logger(__name__)


class Database:
    """
    Database connection manager with retry logic and health checks.
    
    Features:
    - Automatic retry on connection failure
    - Connection pooling with configurable limits
    - Health check verification
    - Graceful connection closure
    """

    client: Optional[AsyncIOMotorClient] = None
    _max_retries: int = 3
    _retry_delay: int = 2  # seconds

    @classmethod
    async def connect_db(cls):
        """
        Initialize database connection and Beanie ODM with retry logic.
        
        Raises:
            ConnectionFailure: If unable to connect after max retries
        """
        last_exception = None
        
        for attempt in range(1, cls._max_retries + 1):
            try:
                logger.info(
                    f"Attempting to connect to MongoDB (Attempt {attempt}/{cls._max_retries})",
                    extra={"attempt": attempt, "max_retries": cls._max_retries}
                )
                
                # Create MongoDB client with production-ready settings
                cls.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=10000,
                    maxPoolSize=50,  # Increased for production
                    minPoolSize=10,
                    maxIdleTimeMS=45000,
                    retryWrites=True,
                    retryReads=True,
                )

                # Verify connection with ping
                await cls.client.admin.command("ping")
                logger.info(
                    "Successfully connected to MongoDB",
                    extra={
                        "database": settings.DATABASE_NAME,
                        "attempt": attempt,
                    }
                )

                # Initialize Beanie ODM
                await init_beanie(
                    database=cls.client[settings.DATABASE_NAME], 
                    document_models=[Product]
                )
                logger.info(
                    "Beanie ODM initialized successfully",
                    extra={"models": ["Product"]}
                )
                
                # Verify database is accessible
                await cls.health_check()
                
                return  # Success - exit the retry loop

            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                last_exception = e
                logger.warning(
                    f"MongoDB connection attempt {attempt} failed: {str(e)}",
                    extra={
                        "attempt": attempt,
                        "max_retries": cls._max_retries,
                        "error_type": type(e).__name__,
                    }
                )
                
                if attempt < cls._max_retries:
                    logger.info(f"Retrying in {cls._retry_delay} seconds...")
                    await asyncio.sleep(cls._retry_delay)
                else:
                    logger.error(
                        f"Failed to connect to MongoDB after {cls._max_retries} attempts",
                        exc_info=True
                    )
                    
            except Exception as e:
                logger.error(
                    f"Unexpected error during database initialization: {str(e)}",
                    exc_info=True,
                    extra={"error_type": type(e).__name__}
                )
                raise
        
        # If we get here, all retries failed
        raise ConnectionFailure(
            f"Failed to connect to MongoDB after {cls._max_retries} attempts: {last_exception}"
        )

    @classmethod
    async def close_db(cls):
        """Close database connection gracefully."""
        if cls.client:
            try:
                cls.client.close()
                logger.info(
                    "MongoDB connection closed successfully",
                    extra={"database": settings.DATABASE_NAME}
                )
            except Exception as e:
                logger.error(
                    f"Error while closing database connection: {str(e)}",
                    exc_info=True
                )
        else:
            logger.warning("Attempted to close database connection, but no client exists")

    @classmethod
    async def get_database(cls):
        """
        Get database instance.
        
        Returns:
            AsyncIOMotorDatabase instance
            
        Raises:
            RuntimeError: If database is not initialized
        """
        if not cls.client:
            logger.error("Attempted to get database before initialization")
            raise RuntimeError("Database not initialized. Call connect_db first.")
        return cls.client[settings.DATABASE_NAME]
    
    @classmethod
    async def health_check(cls) -> bool:
        """
        Perform a health check on the database connection.
        
        Returns:
            True if database is healthy, False otherwise
        """
        try:
            if not cls.client:
                logger.warning("Health check failed: No database client")
                return False
                
            # Ping the database
            await cls.client.admin.command("ping")
            
            # Try to access the database
            db = cls.client[settings.DATABASE_NAME]
            await db.list_collection_names()
            
            logger.debug("Database health check passed")
            return True
            
        except Exception as e:
            logger.error(
                f"Database health check failed: {str(e)}",
                exc_info=True,
                extra={"error_type": type(e).__name__}
            )
            return False


db = Database()
