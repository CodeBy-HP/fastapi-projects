"""
Simple script to manually test the Movie Collection API.
Make sure the server is running before executing this script.

Usage:
    python test_api_manual.py
"""

import httpx
import json
from typing import Optional


BASE_URL = "http://localhost:8000"


def print_response(title: str, response: httpx.Response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint."""
    print("\n🏥 Testing Health Check...")
    response = httpx.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response


def test_create_movie(movie_data: dict) -> Optional[str]:
    """Test creating a new movie."""
    print("\n🎬 Creating a new movie...")
    response = httpx.post(f"{BASE_URL}/movies/", json=movie_data)
    print_response(f"Create Movie: {movie_data['title']}", response)
    
    if response.status_code == 201:
        return response.json()["_id"]
    return None


def test_get_all_movies(page: int = 1, page_size: int = 10):
    """Test getting all movies."""
    print(f"\n📚 Getting all movies (page {page}, size {page_size})...")
    response = httpx.get(
        f"{BASE_URL}/movies/",
        params={"page": page, "page_size": page_size}
    )
    print_response("Get All Movies", response)
    return response


def test_search_movies(title: Optional[str] = None, 
                       director: Optional[str] = None,
                       genre: Optional[str] = None,
                       min_year: Optional[int] = None,
                       max_year: Optional[int] = None):
    """Test searching movies."""
    print("\n🔍 Searching movies...")
    params = {}
    if title:
        params["title"] = title
    if director:
        params["director"] = director
    if genre:
        params["genre"] = genre
    if min_year:
        params["min_year"] = min_year
    if max_year:
        params["max_year"] = max_year
    
    response = httpx.get(f"{BASE_URL}/movies/search", params=params)
    print_response(f"Search Movies: {params}", response)
    return response


def test_get_movie_by_id(movie_id: str):
    """Test getting a specific movie."""
    print(f"\n🎥 Getting movie by ID: {movie_id}...")
    response = httpx.get(f"{BASE_URL}/movies/{movie_id}")
    print_response("Get Movie by ID", response)
    return response


def test_update_movie(movie_id: str, update_data: dict):
    """Test updating a movie."""
    print(f"\n✏️ Updating movie {movie_id}...")
    response = httpx.put(f"{BASE_URL}/movies/{movie_id}", json=update_data)
    print_response("Update Movie", response)
    return response


def test_delete_movie(movie_id: str):
    """Test deleting a movie."""
    print(f"\n🗑️ Deleting movie {movie_id}...")
    response = httpx.delete(f"{BASE_URL}/movies/{movie_id}")
    print_response("Delete Movie", response)
    return response


def run_full_test_suite():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("🚀 MOVIE COLLECTION API - MANUAL TEST SUITE")
    print("="*60)
    
    # Sample movies to create
    movies = [
        {
            "title": "The Shawshank Redemption",
            "director": "Frank Darabont",
            "genre": "Drama",
            "release_year": 1994,
            "rating": 9.3,
            "is_favorite": True
        },
        {
            "title": "The Dark Knight",
            "director": "Christopher Nolan",
            "genre": "Action",
            "release_year": 2008,
            "rating": 9.0,
            "is_favorite": True
        },
        {
            "title": "Inception",
            "director": "Christopher Nolan",
            "genre": "Sci-Fi",
            "release_year": 2010,
            "rating": 8.8,
            "is_favorite": False
        }
    ]
    
    created_movie_ids = []
    
    try:
        # 1. Health Check
        test_health_check()
        
        # 2. Create multiple movies
        for movie in movies:
            movie_id = test_create_movie(movie)
            if movie_id:
                created_movie_ids.append(movie_id)
        
        # 3. Get all movies
        test_get_all_movies()
        
        # 4. Get all movies with sorting
        response = httpx.get(
            f"{BASE_URL}/movies/",
            params={"page": 1, "page_size": 10, "sort_by": "rating", "order": "desc"}
        )
        print_response("Get All Movies (Sorted by Rating DESC)", response)
        
        # 5. Search movies by title
        test_search_movies(title="dark")
        
        # 6. Search movies by director
        test_search_movies(director="nolan")
        
        # 7. Search movies by year range
        test_search_movies(min_year=2000, max_year=2010)
        
        # 8. Get specific movie
        if created_movie_ids:
            test_get_movie_by_id(created_movie_ids[0])
        
        # 9. Update a movie
        if created_movie_ids:
            update_data = {
                "rating": 9.5,
                "is_favorite": False
            }
            test_update_movie(created_movie_ids[0], update_data)
        
        # 10. Test error handling - Invalid ID
        print("\n🔴 Testing error handling with invalid ID...")
        response = httpx.get(f"{BASE_URL}/movies/invalid_id")
        print_response("Get Movie with Invalid ID (Should fail)", response)
        
        # 11. Test validation error - Invalid rating
        print("\n🔴 Testing validation error with invalid rating...")
        invalid_movie = {
            "title": "Invalid Movie",
            "director": "Test",
            "genre": "Drama",
            "release_year": 2020,
            "rating": 15.0,  # Invalid: > 10
            "is_favorite": False
        }
        response = httpx.post(f"{BASE_URL}/movies/", json=invalid_movie)
        print_response("Create Movie with Invalid Rating (Should fail)", response)
        
        # 12. Delete movies (cleanup)
        print("\n🧹 Cleaning up - Deleting created movies...")
        for movie_id in created_movie_ids:
            test_delete_movie(movie_id)
        
        print("\n✅ All tests completed!")
        
    except httpx.ConnectError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python app/main.py")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


def interactive_mode():
    """Interactive testing mode."""
    print("\n🎮 INTERACTIVE MODE")
    print("="*60)
    print("1. Create a movie")
    print("2. Get all movies")
    print("3. Search movies")
    print("4. Get movie by ID")
    print("5. Update movie")
    print("6. Delete movie")
    print("7. Run full test suite")
    print("0. Exit")
    print("="*60)
    
    while True:
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            title = input("Title: ")
            director = input("Director: ")
            genre = input("Genre: ")
            release_year = int(input("Release Year: "))
            rating = float(input("Rating (0-10): "))
            is_favorite = input("Is Favorite (yes/no): ").lower() == "yes"
            
            movie_data = {
                "title": title,
                "director": director,
                "genre": genre,
                "release_year": release_year,
                "rating": rating,
                "is_favorite": is_favorite
            }
            test_create_movie(movie_data)
        elif choice == "2":
            test_get_all_movies()
        elif choice == "3":
            title = input("Search by title (press Enter to skip): ") or None
            director = input("Search by director (press Enter to skip): ") or None
            test_search_movies(title=title, director=director)
        elif choice == "4":
            movie_id = input("Enter Movie ID: ")
            test_get_movie_by_id(movie_id)
        elif choice == "5":
            movie_id = input("Enter Movie ID: ")
            rating = input("New rating (press Enter to skip): ")
            update_data = {}
            if rating:
                update_data["rating"] = float(rating)
            test_update_movie(movie_id, update_data)
        elif choice == "6":
            movie_id = input("Enter Movie ID: ")
            test_delete_movie(movie_id)
        elif choice == "7":
            run_full_test_suite()
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import sys
    
    print("🎬 Movie Collection API - Manual Testing Script")
    print("="*60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        print("\nRunning full test suite...")
        print("(Use --interactive flag for interactive mode)")
        run_full_test_suite()
