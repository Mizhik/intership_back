from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ResultSchema(BaseModel):
    question_id: UUID
    answer_id: list[UUID]


class ResultResponse(BaseModel):
    user_id: UUID
    quiz_id: UUID
    create_at: datetime
    correct_answers: int
    total_questions: int
    score_percentage: int

    class Config:
        from_attributes = True
