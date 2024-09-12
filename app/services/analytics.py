from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.quiz import QuizRepository
from app.repository.analytics import AnalyticsRepository
from app.repository.result import ResultRepository
from app.services.errors import UserForbidden


class AnalyticsService:

    def __init__(
        self,
        db: AsyncSession,
        repository: AnalyticsRepository,
        quiz_repository: QuizRepository,
        result_repository: ResultRepository,
        action_repository: ActionRepository,
    ):
        self.db = db
        self.repository = repository
        self.quiz_repository = quiz_repository
        self.result_repository = (result_repository,)
        self.action_repository = action_repository

    async def calculation_result(self, list):
        total_score = 0
        list_attempts = []

        for quiz in list:
            total_score += quiz.score_percentage
            list_attempts.append(
                {
                    "last_attempt": quiz.create_at,
                    "average_score": round(total_score / (len(list_attempts) + 1), 1),
                    "score_percentage": quiz.score_percentage,
                }
            )

        return list_attempts

    async def get_analytics_user_by_all_quizzes(
        self,
        user_id: UUID,
        current_user: User,
    ):
        if user_id != current_user.id:
            raise UserForbidden

        attempts = await self.repository.get_attempt_by_user(user_id)
        return await self.calculation_result(attempts)

    async def get_analytics_user_by_quiz(
        self, user_id: UUID, quiz_id: UUID, current_user: User
    ):
        if user_id != current_user.id:
            raise UserForbidden

        attempts = await self.repository.get_results_by_quiz(user_id, quiz_id)
        return await self.calculation_result(attempts)

    async def get_analytics_user_by_company(
        self, user_id: UUID, company_id: UUID, current_user: User
    ):
        if user_id != current_user.id:
            raise UserForbidden

        attempts = await self.repository.get_results_by_company(user_id, company_id)
        return await self.calculation_result(attempts)

    async def get_analytics_members_by_date(
        self,
        from_date: datetime,
        to_date: datetime,
        company_id: UUID,
        current_user: User,
    ):
        if not await self.action_repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden

        members_result = await self.repository.get_result_members_by_date(
            from_date, to_date, company_id
        )
        return await self.calculation_result(members_result)

    async def get_analytics_member_by_id(
        self,
        user_id: UUID,
        company_id: UUID,
        current_user: User,
    ):
        if not await self.action_repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden

        member_result = await self.repository.get_result_member_by_id(
            user_id, company_id
        )

        return await self.calculation_result(member_result)

    async def get_analytics_members_last_passing_time(
        self,
        company_id: UUID,
        quiz_id:UUID,
        current_user: User,
    ):
        if not await self.action_repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden

        members_result = await self.repository.get_result_members_last_passing_time(
            company_id, quiz_id
        )

        return members_result
