# 🧪 API Testing Guide

This guide provides multiple ways to test your Movie Collection API during development.

## 🎯 Testing Options

### 1. **FastAPI Interactive Documentation (Recommended for Beginners)**

FastAPI automatically generates interactive API documentation.

#### Steps:
1. Start your server:
   ```bash
   python app/main.py
   ```

2. Open your browser and visit:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

3. In Swagger UI:
   - Click on any endpoint to expand it
   - Click "Try it out"
   - Fill in the parameters/body
   - Click "Execute"
   - View the response

**Pros**: Built-in, no installation needed, great UI
**Cons**: Manual testing only

---

### 2. **Postman (Most Popular)**

Download from: https://www.postman.com/downloads/

#### Quick Start:
1. Create a new Collection called "Movie API"
2. Add requests for each endpoint
3. Set environment variables for base URL

#### Example Request - Create Movie:
```
Method: POST
URL: http://localhost:8000/movies/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "title": "Inception",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "release_year": 2010,
    "rating": 8.8,
    "is_favorite": true
}
```

**Pros**: Professional tool, save requests, organize collections
**Cons**: Requires separate application

---

### 3. **HTTPie (Command Line - Simple)**

Install:
```bash
pip install httpx-cli
# or
pip install httpie
```

#### Examples:

**Create a movie:**
```bash
http POST http://localhost:8000/movies/ \
  title="The Matrix" \
  director="Wachowski Brothers" \
  genre="Sci-Fi" \
  release_year:=1999 \
  rating:=8.7 \
  is_favorite:=true
```

**Get all movies:**
```bash
http GET "http://localhost:8000/movies/?page=1&page_size=10"
```

**Search movies:**
```bash
http GET "http://localhost:8000/movies/search?title=matrix&min_year=1990"
```

**Update a movie:**
```bash
http PUT http://localhost:8000/movies/673e8a3f3b2c1d4e5f6a7b8c \
  rating:=9.0 \
  is_favorite:=true
```

**Delete a movie:**
```bash
http DELETE http://localhost:8000/movies/673e8a3f3b2c1d4e5f6a7b8c
```

**Pros**: Fast, scriptable, beautiful output
**Cons**: Command line only

---

### 4. **cURL (Universal Command Line)**

Available on all systems.

#### Examples:

**Create a movie:**
```bash
curl -X POST "http://localhost:8000/movies/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Interstellar",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "release_year": 2014,
    "rating": 8.6,
    "is_favorite": true
  }'
```

**Get all movies:**
```bash
curl "http://localhost:8000/movies/?page=1&page_size=10"
```

**Search movies:**
```bash
curl "http://localhost:8000/movies/search?title=star&genre=sci-fi"
```

**Get specific movie:**
```bash
curl "http://localhost:8000/movies/673e8a3f3b2c1d4e5f6a7b8c"
```

**Update a movie:**
```bash
curl -X PUT "http://localhost:8000/movies/673e8a3f3b2c1d4e5f6a7b8c" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 9.5,
    "is_favorite": true
  }'
```

**Delete a movie:**
```bash
curl -X DELETE "http://localhost:8000/movies/673e8a3f3b2c1d4e5f6a7b8c"
```

**Pros**: Available everywhere, scriptable
**Cons**: Verbose syntax

---

### 5. **Python Script with httpx/requests**

Create a test script `test_api_manual.py`:

```python
import httpx
import json

BASE_URL = "http://localhost:8000"

def test_create_movie():
    movie_data = {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "genre": "Action",
        "release_year": 2008,
        "rating": 9.0,
        "is_favorite": True
    }
    
    response = httpx.post(f"{BASE_URL}/movies/", json=movie_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_all_movies():
    response = httpx.get(f"{BASE_URL}/movies/")
    print(f"Status: {response.status_code}")
    print(f"Total Movies: {response.json()['total']}")
    return response.json()

def test_search_movies():
    params = {
        "title": "dark",
        "min_year": 2000,
        "page": 1,
        "page_size": 10
    }
    response = httpx.get(f"{BASE_URL}/movies/search", params=params)
    print(f"Status: {response.status_code}")
    print(f"Found: {response.json()['total']} movies")
    return response.json()

if __name__ == "__main__":
    print("=== Testing Movie API ===\n")
    
    print("1. Creating a movie...")
    created_movie = test_create_movie()
    movie_id = created_movie["_id"]
    print(f"Created movie with ID: {movie_id}\n")
    
    print("2. Getting all movies...")
    test_get_all_movies()
    print()
    
    print("3. Searching movies...")
    test_search_movies()
    print()
```

Run with:
```bash
python test_api_manual.py
```

**Pros**: Programmatic, can automate complex workflows
**Cons**: Requires writing code

---

### 6. **Automated Testing with pytest (Best Practice)**

Create `tests/test_movies.py`:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_movie():
    async with AsyncClient(app=app, base_url="http://test") as client:
        movie_data = {
            "title": "Test Movie",
            "director": "Test Director",
            "genre": "Drama",
            "release_year": 2023,
            "rating": 7.5,
            "is_favorite": False
        }
        response = await client.post("/movies/", json=movie_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Movie"
        assert "_id" in data

@pytest.mark.asyncio
async def test_get_all_movies():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/movies/")
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "total" in data

@pytest.mark.asyncio
async def test_search_movies():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/movies/search?title=test")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
```

Install pytest:
```bash
pip install pytest pytest-asyncio
```

Run tests:
```bash
pytest tests/ -v
```

**Pros**: Automated, repeatable, CI/CD ready
**Cons**: Requires setup and understanding of testing

---

## 🎯 Recommended Testing Workflow

For development, I recommend this combination:

1. **Start**: Use **Swagger UI** (http://localhost:8000/docs) for quick manual tests
2. **Intermediate**: Use **Postman** to create a collection of requests you use frequently
3. **Advanced**: Write **pytest** tests for automated testing and CI/CD

---

## 📝 Sample Test Checklist

Use this checklist to test all endpoints:

### Health & Root
- [ ] GET `/` - Should return welcome message
- [ ] GET `/health` - Should return health status

### Create Movie
- [ ] POST `/movies/` with valid data - Should return 201
- [ ] POST `/movies/` with invalid data - Should return 422
- [ ] POST `/movies/` with future year - Should return 422
- [ ] POST `/movies/` with rating > 10 - Should return 422

### Get All Movies
- [ ] GET `/movies/` - Should return paginated list
- [ ] GET `/movies/?page=1&page_size=5` - Should return 5 items
- [ ] GET `/movies/?sort_by=rating&order=desc` - Should sort correctly

### Search Movies
- [ ] GET `/movies/search?title=test` - Should find movies by title
- [ ] GET `/movies/search?director=nolan` - Should find by director
- [ ] GET `/movies/search?min_year=2000&max_year=2010` - Should filter by year range

### Get Single Movie
- [ ] GET `/movies/{valid_id}` - Should return movie
- [ ] GET `/movies/{invalid_id}` - Should return 404

### Update Movie
- [ ] PUT `/movies/{id}` with valid data - Should return 200
- [ ] PUT `/movies/{id}` with invalid data - Should return 422
- [ ] PUT `/movies/{invalid_id}` - Should return 404

### Delete Movie
- [ ] DELETE `/movies/{id}` - Should return success message
- [ ] DELETE `/movies/{invalid_id}` - Should return 404

---

## 🔥 Pro Tips

1. **Use MongoDB Compass** to visualize your data: https://www.mongodb.com/products/compass

2. **Enable Debug Mode**: Set `DEBUG=True` in `.env` for detailed error messages

3. **Check Logs**: FastAPI logs all requests in the terminal

4. **Test Edge Cases**:
   - Empty strings
   - Very long strings
   - Negative numbers
   - Future dates
   - Invalid ObjectIDs

5. **Test Pagination**:
   - First page
   - Last page
   - Page beyond available data

6. **Performance Testing**: Use tools like `locust` or `k6` for load testing

---

## 📚 Additional Resources

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [Postman Learning Center](https://learning.postman.com/)
- [HTTPie Documentation](https://httpie.io/docs)
- [pytest Documentation](https://docs.pytest.org/)

Happy Testing! 🚀
