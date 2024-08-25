from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.result import ResultSchema
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.answer import AnswerRepository
from app.repository.question import QuestionRepository
from app.repository.quiz import QuizRepository
from app.repository.result import ResultRepository
from app.services.errors import UserForbidden
from app.utils.redis import Redis


class ResultService:

    def __init__(
        self,
        db: AsyncSession,
        repository: ResultRepository,
        quiz_repository: QuizRepository,
        answer_repository: AnswerRepository,
        action_repository: ActionRepository,
        question_repository: QuestionRepository,
    ):
        self.db = db
        self.repository = repository
        self.quiz_repository = quiz_repository
        self.answer_repository = answer_repository
        self.action_repository = action_repository
        self.question_repository = question_repository

    async def submit_quiz(
        self,
        quiz_id: UUID,
        user_id: UUID,
        answers_input: list[ResultSchema],
    ):
        quiz = await self.quiz_repository.get_one_or_404({"id": quiz_id})

        await self.action_repository.is_user_member(quiz.company_id, user_id)

        questions = await self.question_repository.get_many_by_params(quiz_id=quiz.id)

        correct_answers = {}
        for question in questions:
            answers = await self.answer_repository.get_many_by_params(
                question_id=question.id, is_correct=True
            )
            correct_answers[question.id] = [answer.id for answer in answers]

        correct_answers_count = 0
        detailed_answers = []
        for user_answer in answers_input:
            question_id = user_answer.question_id
            user_answer_id = user_answer.answer_id

            is_correct = set(user_answer_id) == set(
                correct_answers.get(question_id, [])
            )
            if is_correct:
                correct_answers_count += 1

            question_name = await self.question_repository.get_one(id=question_id)
            answer_name = await self.answer_repository.get_many_by_list(user_answer_id)
            detailed_answers.append(
                {
                    "question": question_name.title,
                    "answer": answer_name,
                    "is_correct": is_correct,
                }
            )
        score_percentage = (correct_answers_count / len(questions)) * 100
        await self.quiz_repository.update(quiz_id, {"frequency": quiz.frequency + 1})
        result = await self.repository.create(
            {
                "user_id": user_id,
                "quiz_id": quiz_id,
                "correct_answers": correct_answers_count,
                "total_questions": len(questions),
                "score_percentage": score_percentage,
            }
        )
        await Redis.save_results_to_redis(result, detailed_answers)
        return result

    async def get_user_average_in_company(
        self, user_id: UUID, company_id: UUID, current_user: User
    ) -> float:
        if (
            user_id != current_user.id
        ) and not await self.action_repository.is_user_owner_or_admin(
            current_user.id, company_id
        ):
            raise UserForbidden

        results = await self.repository.get_results_by_user_and_company(
            user_id, company_id
        )

        if not results:
            return 0.0

        total_score_percentage = sum(result.score_percentage for result in results)

        average_percentage = total_score_percentage / len(results)

        return {"average_percentage": average_percentage}

    async def get_user_average_across_system(
        self, user_id: UUID, current_user: User
    ) -> float:
        if user_id != current_user.id:
            raise UserForbidden
        results = await self.repository.get_results_by_user(user_id)
        if not results:
            return 0.0

        total_score_percentage = sum(result.score_percentage for result in results)

        average_percentage = total_score_percentage / len(results)

        return {"average_percentage_system": average_percentage}
