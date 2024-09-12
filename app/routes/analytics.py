from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.analytics import AnalyticResponse, AnalyticResponseUser
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.quiz import QuizRepository
from app.repository.analytics import AnalyticsRepository
from app.repository.result import ResultRepository
from app.services.auth import AuthService
from app.services.analytics import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])


async def get_analytics_service(db: AsyncSession = Depends(get_db)):
    analytics_repository = AnalyticsRepository(db)
    quiz_repository = QuizRepository(db)
    result_repository = ResultRepository(db)
    action_repository = ActionRepository(db)
    return AnalyticsService(
        db, analytics_repository, quiz_repository, result_repository, action_repository
    )


@router.get("/all-quizzes/{user_id}", response_model=list[AnalyticResponse])
async def analytics_average_score_user_in_system(
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_user_by_all_quizzes(
        user_id, current_user
    )


@router.get("/by-quiz/{quiz_id}", response_model=list[AnalyticResponse])
async def analytics_average_score_user_in_system_by_quiz(
    user_id: UUID,
    quiz_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_user_by_quiz(
        user_id, quiz_id, current_user
    )


@router.get("/by-company/{company_id}", response_model=list[AnalyticResponse])
async def analytics_average_score_user_in_system_by_company(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_user_by_company(
        user_id, company_id, current_user
    )


@router.get("/members/{from_date}/{to_date}")
async def analytics_average_score_members_in_company_by_date(
    from_date: datetime,
    to_date: datetime,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_members_by_date(
        from_date, to_date, company_id, current_user
    )


@router.get("/members/last_passing_time", response_model=list[AnalyticResponseUser])
async def analytics_members_last_passing_time(
    company_id: UUID,
    quiz_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_members_last_passing_time(
        company_id, quiz_id, current_user
    )


@router.get("/members/{user_id}")
async def analytics_average_score_member_in_company_by_id(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    return await analytics_service.get_analytics_member_by_id(
        user_id, company_id, current_user
    )
