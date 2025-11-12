# PROJECT MOVIE COLLECTION API

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

- **Make Beanie Models**
Fields:
    title: str
    director: str
    genre: str
    release_year: int
    rating: float (0–10)
    is_favorite: bool (default=False)

- **Setup database connection**

- **Initialze the Fastapi App lifespan with db methods**

- ***Setup CRUD Schemas***

- **Setup CRUD routes**

- set /health endpoint in main.py

- set exception_handlers in main.py