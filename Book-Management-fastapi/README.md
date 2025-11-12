# Book Management API

A production-grade RESTful API for managing a digital library of books, built with FastAPI, MongoDB, and Beanie ODM.

## 📋 Features

- ✅ **CRUD Operations**: Create, Read, Update, and Delete books
- 🔍 **Advanced Search**: Search by title, author, genre, price range, and publication year
- 📄 **Pagination**: Efficient pagination for large datasets
- 🔀 **Sorting**: Sort by price, year, title, or creation date
- ✔️ **Validation**: Comprehensive input validation using Pydantic v2
- 🚀 **Async**: Built on async/await for high performance
- 🗄️ **MongoDB**: Using Beanie ODM with Motor driver
- 📚 **API Documentation**: Auto-generated interactive docs with Swagger UI

## 🛠️ Tech Stack

- **FastAPI** 0.115.5 - Modern, fast web framework
- **Beanie** 1.27.0 - Async Python ODM for MongoDB
- **Motor** 3.6.0 - Async MongoDB driver
- **Pydantic** 2.10.2 - Data validation using Python type annotations
- **MongoDB** - NoSQL database

## 📁 Project Structure

```
Beanie-mongodb/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   └── database.py         # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── book.py             # Book document model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── book.py             # Book API endpoints
│   └── schemas/
│       ├── __init__.py
│       └── book.py             # Pydantic schemas
├── venv/                       # Virtual environment
├── .env                        # Environment variables
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- MongoDB 4.4 or higher (running locally or remotely)
- Virtual environment (already created as `venv`)

### Installation

1. **Activate the virtual environment**:

   ```bash
   # On Windows (Git Bash)
   source venv/Scripts/activate
   
   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # On Windows (CMD)
   venv\Scripts\activate.bat
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=book_management
   APP_NAME=Book Management API
   APP_VERSION=1.0.0
   DEBUG=True
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

4. **Ensure MongoDB is running**:

   ```bash
   # Check if MongoDB is running
   mongosh --eval "db.version()"
   ```

### Running the Application

1. **Start the FastAPI server**:

   ```bash
   cd app
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**:

   - **API Root**: http://localhost:8000/
   - **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
   - **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/books/` | Create a new book |
| GET | `/books/` | Get all books (with pagination) |
| GET | `/books/search` | Search books with filters |
| GET | `/books/{book_id}` | Get a specific book by ID |
| PUT | `/books/{book_id}` | Update a book by ID |
| DELETE | `/books/{book_id}` | Delete a book by ID |

### Health & Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root with welcome message |
| GET | `/health` | Health check endpoint |

## 📖 Usage Examples

### Create a Book

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

### Get All Books (with pagination)

```bash
curl "http://localhost:8000/books/?page=1&page_size=10&sort_by=price&order=asc"
```

### Search Books

```bash
curl "http://localhost:8000/books/search?author=Rowling&min_price=10&max_price=30"
```

### Get a Book by ID

```bash
curl "http://localhost:8000/books/{book_id}"
```

### Update a Book

```bash
curl -X PUT "http://localhost:8000/books/{book_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 24.99,
    "description": "Updated description"
  }'
```

### Delete a Book

```bash
curl -X DELETE "http://localhost:8000/books/{book_id}"
```

## 🔍 Search & Filter Options

The `/books/search` endpoint supports:

- **title**: Partial match, case-insensitive
- **author**: Partial match, case-insensitive
- **genre**: Partial match, case-insensitive
- **min_price** / **max_price**: Price range filter
- **min_year** / **max_year**: Publication year range
- **page**: Page number (default: 1)
- **page_size**: Items per page (default: 10, max: 100)
- **sort_by**: Sort field (price, published_year, title, created_at)
- **order**: Sort order (asc, desc)

## ✅ Data Validation

The API includes comprehensive validation:

- **Title & Author**: Required, cannot be empty or whitespace
- **Price**: Must be greater than 0, rounded to 2 decimal places
- **Published Year**: Must be between 1000 and current year
- **Description**: Optional, max 2000 characters
- **Genre**: Optional, max 50 characters, auto-capitalized

## 🏗️ Best Practices Implemented

1. **Separation of Concerns**: Models, schemas, routes, and core logic are separated
2. **Type Hints**: Full type annotation throughout the codebase
3. **Async/Await**: All database operations are asynchronous
4. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
5. **Validation**: Pydantic v2 for data validation and serialization
6. **Environment Variables**: Configuration via environment variables
7. **Logging**: Structured logging for debugging and monitoring
8. **CORS**: Configurable CORS middleware
9. **API Documentation**: Auto-generated OpenAPI documentation
10. **Connection Pooling**: Efficient database connection management
11. **Lifecycle Management**: Proper startup and shutdown handling
12. **Input Sanitization**: Trimming whitespace and normalizing data

## 🧪 Testing the API

You can test the API using:

1. **Swagger UI** (recommended): http://localhost:8000/docs
2. **cURL** (see examples above)
3. **Postman** or **Insomnia**: Import the OpenAPI spec from http://localhost:8000/openapi.json
4. **Python requests**:

```python
import requests

# Create a book
response = requests.post(
    "http://localhost:8000/books/",
    json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "published_year": 1925,
        "price": 15.99,
        "genre": "Classic"
    }
)
print(response.json())
```

## 🔒 Production Considerations

Before deploying to production:

1. Set `DEBUG=False` in `.env`
2. Use a secure MongoDB connection string (authentication enabled)
3. Configure proper CORS origins
4. Add authentication/authorization
5. Implement rate limiting
6. Add request logging and monitoring
7. Use environment-specific configuration
8. Set up proper error tracking (e.g., Sentry)
9. Use a production ASGI server (uvicorn with workers)
10. Add database indexes for better performance

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For support, please open an issue in the repository.

---

**Built with ❤️ using FastAPI, MongoDB, and Beanie**
