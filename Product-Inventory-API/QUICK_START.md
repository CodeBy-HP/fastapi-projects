# 🚀 Quick Start Guide

---

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
# At minimum, set your MONGODB_URL
```

### 3. Start MongoDB
```bash
# If using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or use your existing MongoDB instance
```

### 4. Run the Application
```bash
# From the project root
cd Product-Inventory-API
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Create a product
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 14",
    "category": "Electronics",
    "price": 999.99,
    "quantity": 50
  }'

# Get all products
curl http://localhost:8000/products/

# API Documentation
# Open in browser: http://localhost:8000/docs
```

---

## 🔍 See Logging in Action

### Check the Logs
```bash
# Watch logs in real-time
tail -f logs/app.log

# See only errors
tail -f logs/app_error.log

# Search for specific request
grep "request_id=<some-id>" logs/app.log
```

### What You'll See Now
Every request logs:
```
2024-01-15 10:30:45 | INFO | Incoming request: POST /products | request_id=abc-123
2024-01-15 10:30:45 | INFO | Creating new product: iPhone 14
2024-01-15 10:30:45 | INFO | Product created successfully | product_id=507f...
2024-01-15 10:30:45 | INFO | Request completed: Status 201 - Time: 0.145s
```

---

### 4. Request Tracing
Every request gets a unique ID:
```python
# In logs
request_id=abc-123-def-456

# In response headers
X-Request-ID: abc-123-def-456
```

Grep this ID to see the entire request lifecycle!

---

### Test 1: See Request Tracing
```bash
# Make a request
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "category": "Test", "price": 10, "quantity": 1}'

# Check logs - you'll see request_id throughout
tail -20 logs/app.log
```

### Test 2: See Error Logging
```bash
# Try invalid product ID
curl http://localhost:8000/products/invalid-id

# Check error log
tail logs/app_error.log
```

### Test 3: See Validation Logging
```bash
# Send invalid data
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "", "category": "Test", "price": -10, "quantity": 1}'

# Check logs for validation warnings
tail -20 logs/app.log | grep WARNING
```