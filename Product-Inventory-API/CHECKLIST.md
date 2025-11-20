# PROJECT PRODUCT INVENTORY API

- My CheckList for making the project

## Development

- **Make Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate
```

- **Make env file**

```bash
touch .env
```

NOTE - Make sure to set _DEBUG=False_ in env at the time of deployment.

- **Intialize fastapi project**

```bash
pip install fastapi uvicorn motor beanie pydantic python-dotenv httpx requests
```

- Set up middlewares

- **Set config file at app/core/config.py**

- set logger for each File

- **Make Beanie Models**
  Fields:
  name: str
  category: str
  price: float
  quantity: int
  in_stock: bool (auto = quantity > 0)

      - do LOCAL TESTING Of the Beanie document by converting it to pydantic basemodel

- **Setup database connection**

- **Initialze the Fastapi App lifespan with db methods**

- **_Setup CRUD Schemas_**

- **Setup CRUD routes**
- Order of the routes matter
- include routers in main.py

- set /health endpoint in main.py

- set exception_handlers in main.py


## 📋 Project modifications

- ✅ Absolute imports instead of relative
- ✅ Specific exception handling
- ✅ Comprehensive logging with context
- ✅ Request ID tracking
- ✅ Database retry logic
- ✅ Security headers
- ✅ Proper route ordering
- ✅ Environment validation
- ✅ Connection pooling
- ✅ Health checks
- ✅ Type hints everywhere
- ✅ Docstrings for all public functions
- ✅ Environment-specific settings
- ✅ Graceful error messages
