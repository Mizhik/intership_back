from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.database.redis_connector import get_redis_client

from redis import asyncio as aioredis
router = APIRouter(prefix="/healthchecker", tags=["healthchecker"])


@router.get("/")
def root():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@router.get("/db")
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


@router.get("/redis")
async def read_root(redis: aioredis.Redis = Depends(get_redis_client)):
    await redis.set("mykey", "value")
    value = await redis.get("mykey")
    return {"message": f"Value from Redis: {value}"}
