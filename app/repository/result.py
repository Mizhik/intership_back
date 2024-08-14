from uuid import UUID
from sqlalchemy import func, select
from app.repository.base_repository import BaseRepository
from app.entity.models import Quiz, Result


class ResultRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Result)

    async def get_results_by_user_and_company(self, user_id: UUID, company_id: UUID):
        stmt = (
            select(self.model)
            .join(Quiz, Quiz.id == self.model.quiz_id)
            .filter(self.model.user_id == user_id)
            .filter(Quiz.company_id == company_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_results_by_user(self, user_id: UUID):
        stmt = select(self.model).filter(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
