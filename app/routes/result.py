from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.result import ResultResponse, ResultSchema
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.answer import AnswerRepository
from app.repository.question import QuestionRepository
from app.repository.quiz import QuizRepository
from app.repository.result import ResultRepository
from app.services.auth import AuthService
from app.services.result import ResultService


router = APIRouter(prefix="/result", tags=["result"])


async def get_result_service(db: AsyncSession = Depends(get_db)):
    result_repository = ResultRepository(db)
    quiz_repository = QuizRepository(db)
    answer_repository = AnswerRepository(db)
    action_repository = ActionRepository(db)
    question_repository = QuestionRepository(db)
    return ResultService(
        db,
        result_repository,
        quiz_repository,
        answer_repository,
        action_repository,
        question_repository,
    )


@router.post("/", response_model=ResultResponse)
async def submit_quiz(
    quiz_id: UUID,
    answers: list[ResultSchema],
    current_user: User = Depends(AuthService.get_current_user),
    result_service: ResultService = Depends(get_result_service),
):
    return await result_service.submit_quiz(quiz_id, current_user.id, answers)


@router.get("/{user_id}")
async def average_score_user_in_company(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    result_service: ResultService = Depends(get_result_service),
):
    return await result_service.get_user_average_in_company(
        user_id, company_id, current_user
    )


@router.get("/system/{user_id}")
async def average_score_user_in_system(
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    result_service: ResultService = Depends(get_result_service),
):
    return await result_service.get_user_average_across_system(user_id, current_user)


@router.get("/my/download")
async def my_results(
    user_id: UUID,
    file_format: str,
    current_user=Depends(AuthService.get_current_user),
    result_service: ResultService = Depends(get_result_service),
):
    return await result_service.download_user_results(
        user_id, current_user, file_format
    )


@router.get("/member/download")
async def member_results(
    company_id: UUID,
    file_format: str,
    user_id: Optional[UUID] = None,
    quiz_id: Optional[UUID] = None,
    current_user=Depends(AuthService.get_current_user),
    result_service: ResultService = Depends(get_result_service),
):
    return await result_service.download_member_results(
        company_id, current_user, file_format, user_id, quiz_id
    )
