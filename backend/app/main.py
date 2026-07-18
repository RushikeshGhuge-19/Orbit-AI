from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.db.session import SessionLocal

app = FastAPI(
    title="ORBIT AI",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "ORBIT AI Backend"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/db")
async def test_db():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        return {"database": result.scalar()}


app.include_router(auth_router)