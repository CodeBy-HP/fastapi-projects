from fastapi import FastAPI


app = FastAPI()


@app.get(
    "/",
    tags=["Root"],
    summary="API root",
    description="Welcom mesage and API information",
)
async def root() -> dict[str, str]:
    return {"message": "Welcom to Contact-Book-API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
