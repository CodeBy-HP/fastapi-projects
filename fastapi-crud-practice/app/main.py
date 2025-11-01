from fastapi import FastAPI
from app.routes import student_routes

app = FastAPI(title="fastapi-crud-practice", version="1.0.0")

app.include_router(student_routes.router)
