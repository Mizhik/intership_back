from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.quiz import QuizResponseSchema, QuizSchema, QuizUpdate
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.answer import AnswerRepository
from app.repository.company import CompanyRepository
from app.repository.notification import NotificationRepository
from app.repository.question import QuestionRepository
from app.repository.quiz import QuizRepository
from app.services.auth import AuthService
from app.services.quiz import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


async def get_quiz_service(db: AsyncSession = Depends(get_db)):
    quiz_repository = QuizRepository(db)
    action_repository = ActionRepository(db)
    question_repository = QuestionRepository(db)
    answer_repository = AnswerRepository(db)
    notification_repository = NotificationRepository(db)
    company_repository = CompanyRepository(db)
    return QuizService(
        db,
        quiz_repository,
        action_repository,
        question_repository,
        answer_repository,
        notification_repository,
        company_repository,
    )


@router.get("/", response_model=list[QuizResponseSchema])
async def get_quizzes_company(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    quiz_service=Depends(get_quiz_service),
):
    return await quiz_service.get_quizzes_company(company_id, current_user)


@router.post("/", response_model=QuizResponseSchema)
async def create_quiz(
    company_id: UUID,
    body: QuizSchema,
    current_user: User = Depends(AuthService.get_current_user),
    quiz_service=Depends(get_quiz_service),
):
    return await quiz_service.create_quiz(company_id, body, current_user)


@router.patch("/", response_model=QuizResponseSchema)
async def change_quiz(
    quiz_id: UUID,
    body: QuizUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    quiz_service=Depends(get_quiz_service),
):
    return await quiz_service.change_quiz(quiz_id, body, current_user)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    quiz_service=Depends(get_quiz_service),
):
    return await quiz_service.delete_quiz(quiz_id, current_user)
