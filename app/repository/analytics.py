from datetime import datetime
from uuid import UUID
from sqlalchemy import and_, func, select
from app.repository.base_repository import BaseRepository
from app.entity.models import Result


class AnalyticsRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Result)

    async def get_attempt_by_user(self, user_id: UUID):
        stmt = select(self.model).filter(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_results_by_quiz(self, user_id: UUID, quiz_id: UUID):
        stmt = select(self.model).filter(
            self.model.user_id == user_id, self.model.quiz_id == quiz_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_results_by_company(self, user_id: UUID, company_id: UUID):
        stmt = (
            select(self.model)
            .join(self.model.quiz)
            .filter(
                self.model.user_id == user_id,
                self.model.quiz.has(company_id=company_id),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_result_members_by_date(
        self, from_date: datetime, to_date: datetime, company_id: UUID
    ):
        stmt = (
            select(self.model)
            .join(self.model.quiz)
            .filter(
                and_(
                    self.model.quiz.has(company_id=company_id),
                    self.model.create_at >= from_date,
                    self.model.create_at < to_date,
                )
            )
            .group_by(self.model.user_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_result_member_by_id(self, user_id: UUID, company_id: UUID):
        stmt = (
            select(self.model)
            .join(self.model.quiz)
            .filter(
                and_(
                    self.model.quiz.has(company_id=company_id),
                    self.model.user_id == user_id,
                )
            )
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()



    async def get_result_members_last_passing_time(self, company_id: UUID, quiz_id: UUID):
        stmt = (
            select(
                self.model.user_id,
                self.model.quiz_id,
                func.max(self.model.create_at).label("last_attempt"),
            )
            .join(self.model.quiz)
            .filter(
                and_(
                    self.model.quiz.has(company_id=company_id),
                    self.model.quiz_id == quiz_id,
                )
            )
            .group_by(self.model.user_id, self.model.quiz_id)
        )

        result = await self.db.execute(stmt)
        return result.all()
