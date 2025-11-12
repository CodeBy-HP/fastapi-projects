"""
Database configuration and initialization.
Handles MongoDB connection via Motor and Beanie ODM.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging

from app.core.config import settings
from app.models.book import Book

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls) -> None:
        """
        Initialize database connection and Beanie ODM.
        Called on application startup.
        """
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
            
            # Create Motor client
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=10,
                minPoolSize=1
            )
            
            # Test connection
            await cls.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Initialize Beanie with document models
            await init_beanie(
                database=cls.client[settings.DATABASE_NAME],
                document_models=[Book]
            )
            logger.info("Beanie ODM initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls) -> None:
        """
        Close database connection.
        Called on application shutdown.
        """
        if cls.client:
            cls.client.close()
            logger.info("Closed MongoDB connection")


# Database instance
db = Database()
