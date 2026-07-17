from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI(title="ORBIT AI")


@app.get("/")
def root():
    return {"message": "ORBIT AI Backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return {"database": result.scalar()}