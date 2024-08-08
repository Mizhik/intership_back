from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dtos.quiz import QuestionSchema, QuizSchema, QuizUpdate
from app.entity.models import Answer, Question, User
from app.repository.action import ActionRepository
from app.repository.answer import AnswerRepository
from app.repository.question import QuestionRepository
from app.repository.quiz import QuizRepository


class QuizService:

    def __init__(
        self,
        db: AsyncSession,
        repository: QuizRepository,
        action_repository: ActionRepository,
        question_repository: QuestionRepository,
        answer_repository: AnswerRepository,
    ):
        self.db = db
        self.repository = repository
        self.action_repository = action_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository

    async def create_question_with_answers(self, quiz_id: UUID, question_data: QuestionSchema):
        question_dict = {
            "quiz_id": quiz_id,
            "title": question_data.title,
        }
        created_question = await self.question_repository.create(question_dict)

        answer_mappings = [
            Answer(
                question_id=created_question.id,
                title=answer_data.title,
                is_correct=answer_data.is_correct,
            )
            for answer_data in question_data.answers
        ]

        await self.answer_repository.create_many(answer_mappings)
        return created_question

    async def create_quiz(self, company_id: UUID, body: QuizSchema, current_user: User):
        await self.action_repository.is_user_owner_or_admin(company_id, current_user.id)
        quiz_data = body.model_dump(exclude={"questions"})
        quiz_data["company_id"] = company_id
        quiz = await self.repository.create(quiz_data)

        for question_data in body.questions:
            await self.create_question_with_answers(quiz.id, question_data)

        await self.db.commit()
        await self.db.refresh(quiz)
        return quiz

    async def change_quiz(self, quiz_id:UUID, body:QuizUpdate, current_user: User):
        quiz = await self.repository.get_one_or_404({"id": quiz_id})
        await self.action_repository.is_user_owner_or_admin(quiz.company_id, current_user.id)
        return await self.repository.update_many(quiz, body.model_dump(exclude_unset=True))

    async def delete_quiz(self, quiz_id:UUID, current_user: User):
        quiz = await self.repository.get_one_or_404({"id":quiz_id})
        await self.action_repository.is_user_owner_or_admin(quiz.company_id, current_user.id)
        await self.repository.delete_res(quiz.id)

    async def get_quizzes_company(self, company_id:UUID, current_user:User):
        await self.action_repository.is_user_owner_or_admin(company_id, current_user.id)
        return await self.repository.get_many_by_params(company_id=company_id)
