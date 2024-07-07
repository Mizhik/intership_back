import uvicorn
from redis import asyncio as aioredis
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import config
from app.database.db import get_db, get_redis_client
app = FastAPI()

origins = [config.ALLOWED_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@app.get("/api/healthchecker/db")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/api/healthchecker/redis")
async def read_root(redis: aioredis.Redis = Depends(get_redis_client)):
    await redis.set("mykey", "value")
    value = await redis.get("mykey")
    return {"message": f"Value from Redis: {value}"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=config.PORT,
        host=config.HOST,
        reload=config.RELOAD,
        log_level="info",
    )
