from uuid import UUID

from sqlalchemy import select
from app.repository.base_repository import BaseRepository
from app.entity.models import Answer


class AnswerRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Answer)

    async def get_many_by_list(self, id__in: list[UUID]) -> list[Answer]:
        stmt = select(self.model).where(self.model.id.in_(id__in))
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()
