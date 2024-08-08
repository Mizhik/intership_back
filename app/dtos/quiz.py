from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, model_validator


class AnswerSchema(BaseModel):
    title: str
    is_correct: bool


class QuestionSchema(BaseModel):
    title: str
    answers: List[AnswerSchema]

    @model_validator(mode="before")
    def check_answers_count(cls, values):
        answers = values.get("answers", [])
        if len(answers) < 2:
            raise ValueError("Each question must have at least two answer options")

        correct_answers = [answer for answer in answers if answer.get("is_correct")]
        if not correct_answers:
            raise ValueError("Each question must have at least one correct answer")

        return values


class QuizSchema(BaseModel):
    title: str
    description: str
    questions: List[QuestionSchema]

    @model_validator(mode="before")
    def check_questions_count(cls, values):
        if len(values.get("questions", [])) < 2:
            raise ValueError("Each quiz must have at least two questions")
        return values


class AnswerUpdate(BaseModel):
    title: Optional[str]
    is_correct: Optional[bool]


class QuestionUpdate(BaseModel):
    title: Optional[str]
    answers: Optional[List[AnswerUpdate]]

    @model_validator(mode="before")
    def check_answers_count(cls, values):
        answers = values.get("answers", [])
        if len(answers) < 2:
            raise ValueError("Each question must have at least two answer options")

        correct_answers = [answer for answer in answers if answer.get("is_correct")]
        if not correct_answers:
            raise ValueError("Each question must have at least one correct answer")

        return values


class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    questions: Optional[List[QuestionUpdate]]

    @model_validator(mode="before")
    def check_questions_count(cls, values):
        if len(values.get("questions", [])) < 2:
            raise ValueError("Each quiz must have at least two questions")
        return values


class AnswerResponseSchema(BaseModel):
    id: UUID
    title: str
    is_correct: bool


class QuestionResponseSchema(BaseModel):
    id: UUID
    title: str
    answers: List[AnswerResponseSchema]


class QuizResponseSchema(BaseModel):
    id: UUID
    title: str
    description: str
    questions: List[QuestionResponseSchema]
