# 🎬 Movie Collection API

A simple and elegant RESTful API built with FastAPI for managing a personal movie collection.

## 🚀 Features

- ✅ Full CRUD operations for movies
- 📄 Pagination support for listing movies
- 🔍 Advanced search functionality (by title, director, genre, year range)
- 📊 Sorting capabilities
- ⭐ Mark movies as favorites
- 🗄️ MongoDB integration with Beanie ODM
- ✔️ Data validation with Pydantic
- 🛡️ Error handling and exception management
- 📚 Auto-generated API documentation (Swagger/ReDoc)

## 📋 Requirements

- Python 3.8+
- MongoDB 4.0+

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Movie-Collection-API
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=movie_collection_db
APP_NAME=Movie Collection API
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Run the application

```bash
# Using Python
python app/main.py

# Or using Uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 API Endpoints

### Movies

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/movies/` | Create a new movie |
| GET | `/movies/` | Get all movies (with pagination) |
| GET | `/movies/search` | Search movies with filters |
| GET | `/movies/{movie_id}` | Get a specific movie |
| PUT | `/movies/{movie_id}` | Update a movie |
| DELETE | `/movies/{movie_id}` | Delete a movie |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |

## 📊 Example Requests

### Create a Movie

```bash
curl -X POST "http://localhost:8000/movies/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Shawshank Redemption",
    "director": "Frank Darabont",
    "genre": "Drama",
    "release_year": 1994,
    "rating": 9.3,
    "is_favorite": true
  }'
```

### Get All Movies (with pagination)

```bash
curl "http://localhost:8000/movies/?page=1&page_size=10&sort_by=rating&order=desc"
```

### Search Movies

```bash
curl "http://localhost:8000/movies/search?title=shawshank&min_year=1990&max_year=2000"
```

## 🏗️ Project Structure

```
Movie-Collection-API/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Application settings
│   │   └── database.py        # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── movie.py           # Beanie document models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── movie.py           # Pydantic schemas
│   └── routes/
│       ├── __init__.py
│       └── movie.py           # API routes
├── .env                       # Environment variables (not in git)
├── .env.example              # Example environment file
├── .gitignore
├── requirements.txt
├── README.md
└── CHECKLIST.md
```

## 🧪 Testing

For API testing during development, consider:

1. **FastAPI's Interactive Docs** (http://localhost:8000/docs)
2. **Postman** or **Insomnia**
3. **HTTPie** or **curl** commands
4. **pytest** with `httpx` for automated tests

See the Testing Guide section below for detailed instructions.

## 🔒 Security Notes

- Never commit `.env` file to version control
- Change `DEBUG=False` in production
- Use strong MongoDB authentication in production
- Implement rate limiting for production use
- Add authentication/authorization as needed

## 📝 License

MIT License - feel free to use this project for learning purposes!

## 👨‍💻 Author

Your Name - Learning FastAPI Development

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome!
