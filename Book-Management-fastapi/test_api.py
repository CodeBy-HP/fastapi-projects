"""
API Usage Examples for Book Management System
Run these examples to test the API endpoints
"""

import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000"

def print_response(title: str, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response


def create_sample_books():
    """Create sample books"""
    books = [
        {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J.K. Rowling",
            "description": "A young wizard begins his magical education",
            "published_year": 1997,
            "price": 19.99,
            "genre": "Fantasy"
        },
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "description": "A tale of the American Dream in the 1920s",
            "published_year": 1925,
            "price": 15.99,
            "genre": "Classic"
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "A story of racial injustice and childhood innocence",
            "published_year": 1960,
            "price": 14.99,
            "genre": "Classic"
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "description": "A dystopian vision of totalitarian future",
            "published_year": 1949,
            "price": 16.99,
            "genre": "Science Fiction"
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "description": "A fantasy adventure of Bilbo Baggins",
            "published_year": 1937,
            "price": 18.99,
            "genre": "Fantasy"
        }
    ]
    
    book_ids = []
    for book in books:
        response = requests.post(f"{BASE_URL}/books/", json=book)
        print_response(f"Create Book: {book['title']}", response)
        if response.status_code == 201:
            book_ids.append(response.json()["id"])
    
    return book_ids


def get_all_books():
    """Get all books with pagination"""
    response = requests.get(f"{BASE_URL}/books/?page=1&page_size=10")
    print_response("Get All Books (Page 1)", response)
    return response


def get_all_books_sorted():
    """Get all books sorted by price"""
    response = requests.get(
        f"{BASE_URL}/books/?page=1&page_size=10&sort_by=price&order=asc"
    )
    print_response("Get All Books (Sorted by Price ASC)", response)
    return response


def search_books_by_author():
    """Search books by author"""
    response = requests.get(
        f"{BASE_URL}/books/search?author=Rowling"
    )
    print_response("Search Books by Author: Rowling", response)
    return response


def search_books_by_genre():
    """Search books by genre"""
    response = requests.get(
        f"{BASE_URL}/books/search?genre=Fantasy"
    )
    print_response("Search Books by Genre: Fantasy", response)
    return response


def search_books_with_filters():
    """Search books with multiple filters"""
    response = requests.get(
        f"{BASE_URL}/books/search?min_price=15&max_price=20&min_year=1950&sort_by=published_year&order=desc"
    )
    print_response("Search Books (Price: 15-20, Year: 1950+, Sorted by Year)", response)
    return response


def get_book_by_id(book_id):
    """Get a specific book by ID"""
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print_response(f"Get Book by ID: {book_id}", response)
    return response


def update_book(book_id):
    """Update a book"""
    update_data = {
        "price": 21.99,
        "description": "Updated: A young wizard's first year at Hogwarts School of Witchcraft and Wizardry"
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data)
    print_response(f"Update Book: {book_id}", response)
    return response


def delete_book(book_id):
    """Delete a book"""
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    print_response(f"Delete Book: {book_id}", response)
    return response


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🚀 Book Management API - Testing Suite")
    print("="*60)
    
    # Test health check
    print("\n📌 Testing Health Check...")
    test_health_check()
    
    # Create sample books
    print("\n📌 Creating Sample Books...")
    book_ids = create_sample_books()
    
    if not book_ids:
        print("❌ Failed to create books. Please check if the API is running.")
        return
    
    # Get all books
    print("\n📌 Getting All Books...")
    get_all_books()
    
    # Get all books sorted
    print("\n📌 Getting All Books (Sorted)...")
    get_all_books_sorted()
    
    # Search by author
    print("\n📌 Searching by Author...")
    search_books_by_author()
    
    # Search by genre
    print("\n📌 Searching by Genre...")
    search_books_by_genre()
    
    # Search with filters
    print("\n📌 Searching with Multiple Filters...")
    search_books_with_filters()
    
    # Get specific book
    if book_ids:
        print("\n📌 Getting Specific Book...")
        get_book_by_id(book_ids[0])
        
        # Update book
        print("\n📌 Updating Book...")
        update_book(book_ids[0])
        
        # Verify update
        print("\n📌 Verifying Update...")
        get_book_by_id(book_ids[0])
        
        # Delete book
        print("\n📌 Deleting Book...")
        delete_book(book_ids[-1])
        
        # Verify deletion
        print("\n📌 Verifying Remaining Books...")
        get_all_books()
    
    print("\n" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("Please make sure the API is running at http://localhost:8000")
        print("\nTo start the API:")
        print("  - Run: python app/main.py")
        print("  - Or use the start script: ./start.sh or start.bat")
    except Exception as e:
        print(f"\n❌ Error: {e}")
