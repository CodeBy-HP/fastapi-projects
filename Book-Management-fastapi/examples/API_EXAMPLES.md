# API Usage Examples

This directory contains various examples for using the Book Management API.

## Quick Testing with cURL

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Create a Book
```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher'\''s Stone",
    "author": "J.K. Rowling",
    "description": "A young wizard begins his magical education",
    "published_year": 1997,
    "price": 19.99,
    "genre": "Fantasy"
  }'
```

### 3. Get All Books (Paginated)
```bash
# First page, 10 items
curl "http://localhost:8000/books/?page=1&page_size=10"

# With sorting
curl "http://localhost:8000/books/?page=1&page_size=10&sort_by=price&order=asc"
```

### 4. Search Books
```bash
# By author
curl "http://localhost:8000/books/search?author=Rowling"

# By genre
curl "http://localhost:8000/books/search?genre=Fantasy"

# By price range
curl "http://localhost:8000/books/search?min_price=10&max_price=30"

# By year range
curl "http://localhost:8000/books/search?min_year=1990&max_year=2000"

# Combined search
curl "http://localhost:8000/books/search?author=Rowling&min_price=15&max_price=25&sort_by=published_year&order=desc"
```

### 5. Get a Book by ID
```bash
# Replace {book_id} with actual ID from create response
curl "http://localhost:8000/books/{book_id}"
```

### 6. Update a Book
```bash
curl -X PUT "http://localhost:8000/books/{book_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 24.99,
    "description": "Updated description"
  }'
```

### 7. Delete a Book
```bash
curl -X DELETE "http://localhost:8000/books/{book_id}"
```

## Python Examples

Use the `test_api.py` script in the root directory:

```bash
# Make sure the API is running first
cd /c/Users/asus/Desktop/fastapi-projects/Beanie-mongodb
python test_api.py
```

## JavaScript/Node.js Examples

### Using Fetch API

```javascript
// Create a book
async function createBook() {
  const response = await fetch('http://localhost:8000/books/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: "The Great Gatsby",
      author: "F. Scott Fitzgerald",
      published_year: 1925,
      price: 15.99,
      genre: "Classic"
    })
  });
  
  const data = await response.json();
  console.log(data);
  return data;
}

// Get all books
async function getAllBooks() {
  const response = await fetch('http://localhost:8000/books/?page=1&page_size=10');
  const data = await response.json();
  console.log(data);
  return data;
}

// Search books
async function searchBooks(author) {
  const response = await fetch(`http://localhost:8000/books/search?author=${author}`);
  const data = await response.json();
  console.log(data);
  return data;
}

// Update a book
async function updateBook(bookId) {
  const response = await fetch(`http://localhost:8000/books/${bookId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      price: 19.99
    })
  });
  
  const data = await response.json();
  console.log(data);
  return data;
}

// Delete a book
async function deleteBook(bookId) {
  const response = await fetch(`http://localhost:8000/books/${bookId}`, {
    method: 'DELETE'
  });
  
  const data = await response.json();
  console.log(data);
  return data;
}
```

## Postman Collection

You can import the OpenAPI specification into Postman:

1. Open Postman
2. Click "Import"
3. Enter URL: `http://localhost:8000/openapi.json`
4. Postman will automatically create all endpoints

## Advanced Search Examples

### Search by Title (Case-Insensitive)
```bash
curl "http://localhost:8000/books/search?title=potter"
```

### Search by Multiple Criteria
```bash
curl "http://localhost:8000/books/search?genre=Fantasy&min_price=15&max_price=25&sort_by=price&order=desc"
```

### Pagination with Search
```bash
curl "http://localhost:8000/books/search?author=Rowling&page=1&page_size=5"
```

## Testing with HTTPie

If you have HTTPie installed:

```bash
# Create a book
http POST localhost:8000/books/ \
  title="1984" \
  author="George Orwell" \
  published_year:=1949 \
  price:=16.99 \
  genre="Science Fiction"

# Get all books
http GET localhost:8000/books/ page==1 page_size==10

# Search books
http GET localhost:8000/books/search author==Orwell

# Update a book
http PUT localhost:8000/books/{book_id} price:=19.99

# Delete a book
http DELETE localhost:8000/books/{book_id}
```

## Response Examples

### Successful Book Creation (201)
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Harry Potter and the Philosopher's Stone",
  "author": "J.K. Rowling",
  "description": "A young wizard begins his magical education",
  "published_year": 1997,
  "price": 19.99,
  "genre": "Fantasy",
  "created_at": "2024-11-09T10:30:00Z"
}
```

### Book List Response (200)
```json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "books": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Harry Potter and the Philosopher's Stone",
      "author": "J.K. Rowling",
      "published_year": 1997,
      "price": 19.99,
      "genre": "Fantasy",
      "created_at": "2024-11-09T10:30:00Z"
    }
  ]
}
```

### Error Response (404)
```json
{
  "detail": "Book with ID 507f1f77bcf86cd799439011 not found"
}
```

### Validation Error (422)
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "body -> price",
      "message": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```
