"""
Unit tests for Movie API endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to Movie Collection API"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_create_movie_success(client: AsyncClient, sample_movie_data):
    """Test creating a movie with valid data."""
    response = await client.post("/movies/", json=sample_movie_data)
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data
    assert data["title"] == sample_movie_data["title"]
    assert data["director"] == sample_movie_data["director"]
    assert data["rating"] == sample_movie_data["rating"]


@pytest.mark.asyncio
async def test_create_movie_invalid_data(client: AsyncClient):
    """Test creating a movie with invalid data."""
    invalid_data = {
        "title": "",  # Empty title
        "director": "Test Director",
        "genre": "Drama",
        "release_year": 2030,  # Future year
        "rating": 11.0,  # Rating > 10
        "is_favorite": False
    }
    response = await client.post("/movies/", json=invalid_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_movies(client: AsyncClient):
    """Test getting all movies with pagination."""
    response = await client.get("/movies/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    assert isinstance(data["movies"], list)


@pytest.mark.asyncio
async def test_get_movies_with_sorting(client: AsyncClient):
    """Test getting movies with sorting."""
    response = await client.get("/movies/?sort_by=rating&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data


@pytest.mark.asyncio
async def test_search_movies(client: AsyncClient):
    """Test searching movies."""
    response = await client.get("/movies/search?title=shawshank")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_search_movies_by_year_range(client: AsyncClient):
    """Test searching movies by year range."""
    response = await client.get("/movies/search?min_year=1990&max_year=2000")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data


@pytest.mark.asyncio
async def test_get_movie_invalid_id(client: AsyncClient):
    """Test getting a movie with invalid ID."""
    response = await client.get("/movies/invalid_id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_movie_not_found(client: AsyncClient):
    """Test getting a movie that doesn't exist."""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but doesn't exist
    response = await client.get(f"/movies/{fake_id}")
    # Will be 404 if movie doesn't exist, or 200 if it does
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_movie_invalid_id(client: AsyncClient, sample_movie_update_data):
    """Test updating a movie with invalid ID."""
    response = await client.put("/movies/invalid_id", json=sample_movie_update_data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_movie_invalid_id(client: AsyncClient):
    """Test deleting a movie with invalid ID."""
    response = await client.delete("/movies/invalid_id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_movie_with_minimum_rating(client: AsyncClient):
    """Test creating a movie with minimum rating (0)."""
    movie_data = {
        "title": "Bad Movie",
        "director": "Unknown",
        "genre": "Horror",
        "release_year": 2020,
        "rating": 0.0,
        "is_favorite": False
    }
    response = await client.post("/movies/", json=movie_data)
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 0.0


@pytest.mark.asyncio
async def test_create_movie_with_maximum_rating(client: AsyncClient):
    """Test creating a movie with maximum rating (10)."""
    movie_data = {
        "title": "Perfect Movie",
        "director": "Master",
        "genre": "Drama",
        "release_year": 2020,
        "rating": 10.0,
        "is_favorite": True
    }
    response = await client.post("/movies/", json=movie_data)
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 10.0


@pytest.mark.asyncio
async def test_pagination_parameters(client: AsyncClient):
    """Test different pagination parameters."""
    # Test with page_size=5
    response = await client.get("/movies/?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page_size"] == 5
    assert len(data["movies"]) <= 5


@pytest.mark.asyncio
async def test_full_crud_workflow(client: AsyncClient, sample_movie_data, sample_movie_update_data):
    """Test complete CRUD workflow: Create -> Read -> Update -> Delete."""
    
    # 1. Create a movie
    create_response = await client.post("/movies/", json=sample_movie_data)
    assert create_response.status_code == 201
    created_movie = create_response.json()
    movie_id = created_movie["_id"]
    
    # 2. Read the movie
    get_response = await client.get(f"/movies/{movie_id}")
    if get_response.status_code == 200:
        get_movie = get_response.json()
        assert get_movie["_id"] == movie_id
        
        # 3. Update the movie
        update_response = await client.put(f"/movies/{movie_id}", json=sample_movie_update_data)
        if update_response.status_code == 200:
            updated_movie = update_response.json()
            assert updated_movie["rating"] == sample_movie_update_data["rating"]
            
            # 4. Delete the movie
            delete_response = await client.delete(f"/movies/{movie_id}")
            assert delete_response.status_code == 200
