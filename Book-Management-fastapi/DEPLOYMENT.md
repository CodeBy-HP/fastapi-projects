# Production Deployment Guide

## 📋 Pre-Deployment Checklist

### 1. Security Configuration

- [ ] Set `DEBUG=False` in production
- [ ] Use strong MongoDB authentication
- [ ] Configure proper CORS origins
- [ ] Use HTTPS/TLS for all connections
- [ ] Set up environment variable encryption
- [ ] Enable MongoDB authentication and authorization
- [ ] Use secrets management (e.g., AWS Secrets Manager, Azure Key Vault)

### 2. Database Configuration

#### MongoDB Atlas (Recommended for Production)

1. **Create a MongoDB Atlas Cluster**
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Create a new cluster
   - Configure IP whitelist
   - Create database user with appropriate permissions

2. **Update `.env` file**
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=book_management_prod
   DEBUG=False
   ```

#### Self-Hosted MongoDB

```bash
# Enable authentication
mongod --auth --port 27017 --dbpath /data/db

# Create admin user
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: "secure_password",
  roles: ["userAdminAnyDatabase", "readWriteAnyDatabase"]
})

# Create application user
use book_management
db.createUser({
  user: "bookapp",
  pwd: "secure_app_password",
  roles: [{ role: "readWrite", db: "book_management" }]
})

# Update connection string
MONGODB_URL=mongodb://bookapp:secure_app_password@localhost:27017/book_management?authSource=book_management
```

### 3. Application Configuration

#### Production `.env` File

```env
# MongoDB Configuration
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=book_management_prod

# Application Configuration
APP_NAME=Book Management API
APP_VERSION=1.0.0
DEBUG=False

# CORS Settings
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Optional: Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Optional: Logging
LOG_LEVEL=WARNING
```

## 🚀 Deployment Options

### Option 1: Docker Deployment

#### Create `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - DATABASE_NAME=book_management
    depends_on:
      - mongodb
    restart: unless-stopped

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secure_password
    restart: unless-stopped

volumes:
  mongodb_data:
```

#### Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Scale workers
docker-compose up -d --scale api=4
```

### Option 2: Cloud Platform Deployment

#### Heroku

1. **Create `Procfile`**
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
   ```

2. **Deploy**
   ```bash
   heroku create your-book-api
   heroku config:set MONGODB_URL=your_mongodb_atlas_url
   heroku config:set DEBUG=False
   git push heroku main
   ```

#### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   eb init -p python-3.12 book-management-api
   eb create production-env
   eb setenv MONGODB_URL=your_url DEBUG=False
   eb deploy
   ```

#### Google Cloud Run

1. **Create `Dockerfile`** (same as above)

2. **Deploy**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/book-api
   gcloud run deploy book-api \
     --image gcr.io/PROJECT_ID/book-api \
     --platform managed \
     --set-env-vars MONGODB_URL=your_url,DEBUG=False
   ```

#### Azure App Service

```bash
az webapp up --name book-api --resource-group myResourceGroup \
  --runtime "PYTHON:3.12" \
  --sku B1
az webapp config appsettings set --name book-api \
  --resource-group myResourceGroup \
  --settings MONGODB_URL=your_url DEBUG=False
```

### Option 3: VPS Deployment (Ubuntu/Debian)

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.12 python3.12-venv python3-pip -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

# Install Nginx
sudo apt install nginx -y
```

#### 2. Deploy Application

```bash
# Clone/copy project
cd /var/www
sudo git clone your-repo book-api
cd book-api

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
sudo nano .env
# Add your production configuration
```

#### 3. Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/book-api.service
```

```ini
[Unit]
Description=Book Management API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/book-api
Environment="PATH=/var/www/book-api/venv/bin"
ExecStart=/var/www/book-api/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start book-api
sudo systemctl enable book-api
sudo systemctl status book-api
```

#### 4. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/book-api
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/book-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

## 🔒 Security Best Practices

### 1. Environment Variables

Never commit `.env` file. Use secret management services:

```python
# Example with AWS Secrets Manager
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='book-api/prod')
    return json.loads(response['SecretString'])
```

### 2. Rate Limiting

Install slowapi:
```bash
pip install slowapi
```

Add to `main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/books/")
@limiter.limit("60/minute")
async def get_books(request: Request):
    # Your code
```

### 3. API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/books/")
async def get_books(api_key: str = Depends(get_api_key)):
    # Your code
```

### 4. Input Sanitization

Already implemented via Pydantic validators in the models.

### 5. HTTPS Only

Force HTTPS in production:
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)
```

## 📊 Monitoring and Logging

### 1. Application Monitoring

Install Sentry:
```bash
pip install sentry-sdk
```

Add to `main.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

### 2. Structured Logging

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 3. Metrics Collection

Install prometheus client:
```bash
pip install prometheus-client
```

Add metrics endpoint:
```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

## 🎯 Performance Optimization

### 1. Connection Pooling

Already configured in `database.py`:
```python
cls.client = AsyncIOMotorClient(
    settings.MONGODB_URL,
    maxPoolSize=10,  # Adjust based on load
    minPoolSize=1
)
```

### 2. Database Indexing

Indexes are defined in the Book model. Ensure they're created:
```python
# Run once during deployment
await Book.get_motor_collection().create_indexes()
```

### 3. Caching

Install Redis cache:
```bash
pip install fastapi-cache2 redis
```

Add caching:
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="book-cache")

@app.get("/books/")
@cache(expire=60)  # Cache for 60 seconds
async def get_books():
    # Your code
```

### 4. Worker Processes

Use multiple workers in production:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Calculate workers: `(2 × CPU cores) + 1`

## 🧪 Testing in Production

### Health Checks

Already implemented at `/health`. Monitor this endpoint.

### Smoke Tests

```bash
#!/bin/bash
# smoke_test.sh

API_URL="https://your-api.com"

# Health check
curl -f $API_URL/health || exit 1

# Create test book
BOOK_ID=$(curl -s -X POST "$API_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","author":"Test","published_year":2024,"price":9.99}' \
  | jq -r '.id')

# Verify creation
curl -f "$API_URL/books/$BOOK_ID" || exit 1

# Cleanup
curl -X DELETE "$API_URL/books/$BOOK_ID"

echo "✅ Smoke tests passed"
```

## 📈 Scaling Strategies

### Horizontal Scaling

1. **Load Balancer**: Use Nginx, HAProxy, or cloud load balancers
2. **Multiple Instances**: Run multiple API instances
3. **Database Sharding**: Use MongoDB sharding for large datasets
4. **Read Replicas**: Configure MongoDB replica sets

### Vertical Scaling

1. **Increase Resources**: More CPU, RAM for the server
2. **Optimize Queries**: Use explain() to analyze slow queries
3. **Database Tuning**: Optimize MongoDB configuration

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
      
      - name: Deploy to server
        run: |
          # Your deployment commands
```

## 📝 Backup Strategy

### MongoDB Backups

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --uri="$MONGODB_URL" --out="/backups/backup_$DATE"
# Upload to S3
aws s3 cp "/backups/backup_$DATE" "s3://your-bucket/backups/"
```

### Backup Rotation

Keep:
- Daily backups for 7 days
- Weekly backups for 4 weeks
- Monthly backups for 12 months

---

**Remember**: Always test in a staging environment before production deployment!
