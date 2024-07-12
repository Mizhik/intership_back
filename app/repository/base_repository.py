from typing import Optional, TypeVar
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class ErrorNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


class BaseRepository:

    def __init__(self, model: ModelType, db: AsyncSession):
        self.db = db
        self.model = model

    async def get_many(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[ModelType]:
        stmt = select(self.model)
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_one(self, id):
        stmt = select(self.model).filter_by(id=id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, body: dict) -> ModelType:
        result = self.model(**body)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update(self, id: UUID, body: dict) -> ModelType:
        result = await self.get_one_or_404(id)
        if result:
            for key, value in body.items():
                if hasattr(result, key) and value is not None:
                    setattr(result, key, value)
            await self.db.commit()
            await self.db.refresh(result)
        return result

    async def delete_res(self, id: UUID) -> None:
        result = await self.get_one_or_404(id)
        if result:
            await self.db.delete(result)
            await self.db.commit()
        return result

    async def get_one_or_404(self, id: UUID) -> ModelType | None:
        result = await self.get_one(id)
        if not result:
            raise ErrorNotFound
        return result
