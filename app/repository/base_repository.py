from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, model, db: AsyncSession):
        self.db = db
        self.model = model
        
    async def get_many(self, offset, limit):
        stmt = select(self.model).offset(offset).limit(limit)  # без offset limit
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_one(self, id):
        stmt = select(self.model).filter_by(id=id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, body):
        result = self.model(**body.model_dump())
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update(self, id, body):
        result = await self.get_one(id)
        if result:
            for key, value in body.model_dump().items():
                if hasattr(result, key) and value is not None:
                    setattr(result, key, value)
            await self.db.commit()
            await self.db.refresh(result)
        return result
    
    async def delete_res(self, id):
        result = await self.get_one(id)
        if result:
            await self.db.delete(result)
            await self.db.commit()
        return result