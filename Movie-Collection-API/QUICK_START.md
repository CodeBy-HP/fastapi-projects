# 🚀 Quick Start Guide

Get your Movie Collection API up and running in minutes!

## Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher (running locally or cloud)
- Terminal/Command Prompt

---

## 📦 Step 1: Setup Environment

### 1. Create and activate virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Step 2: Configure Environment

### 1. Create `.env` file

Copy the example file:
```bash
cp .env.example .env
```

### 2. Edit `.env` with your settings

Open `.env` in your favorite editor and update:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=movie_collection_db

# Application Configuration
APP_NAME=Movie Collection API
APP_VERSION=1.0.0
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

**Note**: If using MongoDB Atlas (cloud), your MONGODB_URL will look like:
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

## 🎬 Step 3: Run the Application

```bash
python app/main.py
```

You should see:
```
✅ Successfully connected to MongoDB.
✅ Beanie ODM initialized successfully.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🧪 Step 4: Test the API

### Option 1: Use Swagger UI (Easiest)

1. Open your browser
2. Go to: http://localhost:8000/docs
3. Try the endpoints interactively!

### Option 2: Use the Manual Test Script

In a new terminal (keep the server running):

```bash
python test_api_manual.py
```

For interactive mode:
```bash
python test_api_manual.py --interactive
```

### Option 3: Use Postman

1. Download Postman: https://www.postman.com/downloads/
2. Import the collection: `Movie_Collection_API.postman_collection.json`
3. Start testing!

### Option 4: Use cURL

```bash
# Create a movie
curl -X POST "http://localhost:8000/movies/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "release_year": 2010,
    "rating": 8.8,
    "is_favorite": true
  }'

# Get all movies
curl "http://localhost:8000/movies/"

# Health check
curl "http://localhost:8000/health"
```

---

## 🧪 Step 5: Run Automated Tests (Optional)

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

---

## 📖 Step 6: Explore the API

### Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |
| `/movies/` | POST | Create a movie |
| `/movies/` | GET | Get all movies (paginated) |
| `/movies/search` | GET | Search movies |
| `/movies/{id}` | GET | Get specific movie |
| `/movies/{id}` | PUT | Update a movie |
| `/movies/{id}` | DELETE | Delete a movie |

### Documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ Troubleshooting

### MongoDB Connection Issues

**Error**: `❌ Database connection failed`

**Solutions**:
1. Make sure MongoDB is running
2. Check your MONGODB_URL in `.env`
3. For local MongoDB: `mongodb://localhost:27017`
4. For MongoDB Atlas: Use connection string from Atlas dashboard

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change the port in `app/main.py`:
```python
uvicorn.run(
    "main:app",
    host="127.0.0.1",
    port=8001,  # Change this
    reload=settings.DEBUG,
)
```

### Module Import Errors

**Error**: `ModuleNotFoundError`

**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Invalid ObjectId Errors

**Error**: `Invalid movie ID format`

**Solution**: Make sure you're using a valid MongoDB ObjectId (24 character hex string)

---

## 🎯 Next Steps

1. ✅ **Read** the `CODE_REVIEW.md` for detailed code analysis
2. ✅ **Read** the `TESTING_GUIDE.md` for testing strategies
3. ✅ **Explore** the API using Swagger UI
4. ✅ **Customize** the movie model with additional fields
5. ✅ **Add** authentication (JWT) for production use
6. ✅ **Deploy** to a cloud platform (Heroku, Railway, Render)

---

## 📚 Documentation Files

- `README.md` - Comprehensive project documentation
- `CODE_REVIEW.md` - Detailed code review and recommendations
- `TESTING_GUIDE.md` - Complete testing guide with examples
- `CHECKLIST.md` - Original development checklist
- `QUICK_START.md` - This file!

---

## 🆘 Need Help?

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Beanie Docs**: https://beanie-odm.dev/
- **MongoDB Docs**: https://www.mongodb.com/docs/

---

## 🎉 Success!

If you see this, congratulations! Your Movie Collection API is running successfully! 🚀

Now go ahead and:
1. Create some movies
2. Search for them
3. Update ratings
4. Mark favorites

Happy coding! 💻
