from typing import Optional

from sqlalchemy import select
from app.repository.base_repository import BaseRepository
from app.entity.models import Company


class CompanyRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Company)

    async def get_many_with_is_visible(self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[Company]:
        stmt = select(self.model).filter(Company.is_visible == True)
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit).filter(Company.is_visible == True)
        result = await self.db.execute(stmt)
        return result.scalars().all()
