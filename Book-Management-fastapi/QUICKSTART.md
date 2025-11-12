# 📚 Book Management API - Quick Start Guide

## 🎯 What You've Got

A production-grade Book Management API with:
- ✅ Full CRUD operations
- ✅ Advanced search with filters
- ✅ Pagination and sorting
- ✅ Comprehensive validation
- ✅ Production-ready error handling
- ✅ Auto-generated API documentation

## 🚀 Quick Start (3 Steps)

### Step 1: Ensure MongoDB is Running

```bash
# Check if MongoDB is running
mongosh --eval "db.version()"

# If not running, start it:
# Windows: net start MongoDB
# Or: mongod
```

### Step 2: Start the API

Choose one method:

**Option A: Bash (Git Bash/WSL)**
```bash
./start.sh
```

**Option B: PowerShell**
```powershell
.\start.ps1
```

**Option C: CMD**
```cmd
start.bat
```

**Option D: Manual**
```bash
# Activate virtual environment
source venv/Scripts/activate  # Bash
# OR
.\venv\Scripts\Activate.ps1   # PowerShell

# Run the app
cd app
python main.py
```

### Step 3: Access the API

Open your browser:
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## 🎮 Try It Out (Swagger UI)

1. Go to http://localhost:8000/docs
2. Click on **POST /books/** to expand
3. Click **"Try it out"**
4. Use this example data:
   ```json
   {
     "title": "Harry Potter and the Philosopher's Stone",
     "author": "J.K. Rowling",
     "description": "A young wizard begins his magical education",
     "published_year": 1997,
     "price": 19.99,
     "genre": "Fantasy"
   }
   ```
5. Click **"Execute"**
6. See the created book with its ID in the response!

## 📖 All Available Endpoints

### 📚 Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/books/` | Create a new book |
| `GET` | `/books/` | Get all books (paginated) |
| `GET` | `/books/search` | Search books with filters |
| `GET` | `/books/{book_id}` | Get a specific book |
| `PUT` | `/books/{book_id}` | Update a book |
| `DELETE` | `/books/{book_id}` | Delete a book |

### ℹ️ System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |

## 🔍 Search Examples

### By Author
```
GET /books/search?author=Rowling
```

### By Genre
```
GET /books/search?genre=Fantasy
```

### By Price Range
```
GET /books/search?min_price=15&max_price=25
```

### By Year Range
```
GET /books/search?min_year=1990&max_year=2000
```

### Combined Search with Sorting
```
GET /books/search?author=Rowling&min_price=15&max_price=30&sort_by=published_year&order=desc
```

## 🧪 Test the API

Run the automated test script:

```bash
# First, make sure the API is running
python test_api.py
```

This will:
- ✅ Create sample books
- ✅ Test all CRUD operations
- ✅ Test search functionality
- ✅ Test pagination and sorting
- ✅ Clean up test data

## 📁 Project Structure

```
Beanie-mongodb/
├── app/
│   ├── main.py              # 🚀 Application entry point
│   ├── core/
│   │   ├── config.py        # ⚙️ Configuration
│   │   └── database.py      # 🗄️ Database connection
│   ├── models/
│   │   └── book.py          # 📚 Book database model
│   ├── routes/
│   │   └── book.py          # 🛣️ API endpoints
│   └── schemas/
│       └── book.py          # 📋 Request/Response schemas
├── examples/
│   └── API_EXAMPLES.md      # 📖 Usage examples
├── venv/                    # 🐍 Virtual environment
├── .env                     # 🔐 Environment variables
├── requirements.txt         # 📦 Dependencies
├── README.md               # 📘 Full documentation
├── DEPLOYMENT.md           # 🚀 Deployment guide
└── test_api.py             # 🧪 Test script
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# MongoDB Connection
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=book_management

# Application Settings
APP_NAME=Book Management API
APP_VERSION=1.0.0
DEBUG=True

# CORS (for frontend apps)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## ✅ Book Data Validation

The API validates:

- ✅ **Title & Author**: Required, not empty
- ✅ **Price**: Must be > 0, rounded to 2 decimals
- ✅ **Published Year**: Between 1000 and current year
- ✅ **Description**: Optional, max 2000 characters
- ✅ **Genre**: Optional, max 50 characters

## 🎯 Common Use Cases

### 1. Add Books to Your Library
```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Book Title",
    "author": "Author Name",
    "published_year": 2024,
    "price": 29.99,
    "genre": "Technology"
  }'
```

### 2. Find All Fantasy Books
```bash
curl "http://localhost:8000/books/search?genre=Fantasy"
```

### 3. Get Cheap Books (Under $20)
```bash
curl "http://localhost:8000/books/search?max_price=20&sort_by=price&order=asc"
```

### 4. Find Recent Books (2020+)
```bash
curl "http://localhost:8000/books/search?min_year=2020&sort_by=published_year&order=desc"
```

## 🐛 Troubleshooting

### Can't connect to MongoDB?
```bash
# Check if MongoDB is running
mongosh --eval "db.version()"

# Start MongoDB
# Windows: net start MongoDB
# Linux/Mac: sudo systemctl start mongod
```

### Import errors?
```bash
# Reinstall dependencies
source venv/Scripts/activate
pip install -r requirements.txt
```

### Port 8000 already in use?
```bash
# Change port in app/main.py (line 163):
uvicorn.run("main:app", host="0.0.0.0", port=8001)  # Use 8001 instead
```

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **API Examples**: See `examples/API_EXAMPLES.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Interactive Docs**: http://localhost:8000/docs (when running)

## 💡 Next Steps

1. ✅ Start the API and explore the Swagger UI
2. ✅ Create some test books
3. ✅ Try different search queries
4. ✅ Integrate with your frontend application
5. ✅ Deploy to production (see `DEPLOYMENT.md`)

## 🎓 Best Practices Used

This project implements:
- ✅ **Clean Architecture**: Separation of concerns
- ✅ **Type Safety**: Full type hints throughout
- ✅ **Async/Await**: Non-blocking database operations
- ✅ **Validation**: Pydantic v2 for data validation
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Documentation**: Auto-generated OpenAPI docs
- ✅ **Security**: Input validation and sanitization
- ✅ **Scalability**: Connection pooling and async operations

## 🤝 Need Help?

- Check the logs in the terminal where the API is running
- Use Swagger UI to test endpoints interactively
- Review the examples in `examples/API_EXAMPLES.md`
- Check MongoDB connection in `.env` file

---

**🎉 You're all set! Happy coding!**

Built with ❤️ using FastAPI, MongoDB & Beanie
