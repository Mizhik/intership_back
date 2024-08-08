from typing import Optional, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.services.errors import ErrorNotFound

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseRepository:

    def __init__(self, model: ModelType, db: AsyncSession):
        self.db = db
        self.model = model

    async def get_many(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[ModelType]:
        stmt = select(self.model)
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_one(self, **params) -> ModelType:
        query = select(self.model).filter_by(**params)
        result = await self.db.execute(query)
        db_row = result.unique().scalar_one_or_none()
        return db_row

    async def create(self, body: dict) -> ModelType:
        result = self.model(**body)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update(self, id: UUID, body: dict) -> ModelType:
        result = await self.get_one_or_404({"id": id})
        for key, value in body.items():
            if hasattr(result, key) and value is not None:
                setattr(result, key, value)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update_many(self, instance: ModelType, body: dict) -> ModelType:
        await self.update_recursive(instance, body)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update_recursive(self, instance: ModelType, body: dict):
        for key, value in body.items():
            if isinstance(value, dict):
                sub_instance = getattr(instance, key)
                await self.update_recursive(sub_instance, value)
            elif isinstance(value, list):
                for item, sub_instance in zip(value, getattr(instance, key)):
                    await self.update_recursive(sub_instance, item)
            elif hasattr(instance, key) and value is not None:
                setattr(instance, key, value)

    async def delete_res(self, id: UUID) -> None:
        result = await self.get_one_or_404({"id": id})
        await self.db.delete(result)
        await self.db.commit()
        return result

    async def get_one_or_404(self, params: dict) -> ModelType | None:
        result = await self.get_one(**params)
        if not result:
            raise ErrorNotFound
        return result

    async def create_many(self, objects: list[ModelType]) -> list[ModelType]:
        self.db.add_all(objects)
        await self.db.commit()
        for obj in objects:
            await self.db.refresh(obj)
        return objects

    async def get_many_by_params(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **params,
    ) -> list[ModelType]:
        stmt = select(self.model).filter_by(**params)
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()

    # async def get_many_by_params(self, **params) -> list[ModelType]:
    #     query = select(self.model).filter_by(**params)
    #     result = await self.db.execute(query)
    #     return result.unique().scalars().all()
