from typing import Optional

from beanie import init_beanie
from app.core.config import settings
from app.models.movie import Movie
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    """Database connection manager."""

    client: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def connect_db(cls):
        """Initialize database connection and Beanie ODM."""
        try:
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=10, 
                minPoolSize=1,
            )

            # Test connection
            await cls.client.admin.command("ping")
            print("✅ Successfully connected to MongoDB.")

            # Initialize Beanie
            await init_beanie(
                database=cls.client[settings.DATABASE_NAME],
                document_models=[Movie],
            )
            print("✅ Beanie ODM initialized successfully.")

        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            print("🛑 Closed MongoDB connection.")


db = Database()
