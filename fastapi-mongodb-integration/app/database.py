# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file in the app directory

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URL or not DATABASE_NAME:
    raise ValueError("MONGO_URL and DATABASE_NAME must be set in .env")

# Initialize Motor client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]


# Function to get any collection safely
def get_collection(collection_name: str):
    """
    Returns a Motor collection object for async operations.

    Args:
        collection_name (str): Name of the MongoDB collection

    Returns:
        AsyncIOMotorCollection: Motor collection object
    """
    if not collection_name:
        raise ValueError("collection_name must be a non-empty string")
    return db[collection_name]
