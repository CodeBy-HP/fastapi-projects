"""
Pytest configuration and fixtures for testing the Movie Collection API.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_movie_data():
    """Sample movie data for testing."""
    return {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "genre": "Drama",
        "release_year": 1994,
        "rating": 9.3,
        "is_favorite": True
    }


@pytest.fixture
def sample_movie_update_data():
    """Sample movie update data for testing."""
    return {
        "rating": 9.5,
        "is_favorite": False
    }
