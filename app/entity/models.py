from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.entity.base_models import Base
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.entity.enums import ActionStatus


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    actions:Mapped[list["Action"]] = relationship("Action", back_populates='user', lazy="selectin")
    results: Mapped[list["Result"]] = relationship("Result", back_populates="user", lazy="selectin")

class Company(Base):
    __tablename__ = "companies"
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    actions: Mapped[list["Action"]] = relationship("Action", back_populates='company', lazy="selectin")
    quizzes: Mapped[list["Quiz"]] = relationship("Quiz", back_populates="company", cascade="all, delete-orphan")

class Action(Base):
    __tablename__ = "actions"
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    status: Mapped[ActionStatus] = mapped_column('status', Enum(ActionStatus), default=None)
    user: Mapped["User"] = relationship("User", back_populates="actions")
    company: Mapped["Company"] = relationship("Company", back_populates="actions")

class Quiz(Base):
    __tablename__ = "quizzes"
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, default=0)
    company_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    company: Mapped["Company"] = relationship("Company", back_populates="quizzes", lazy="selectin")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="quiz", lazy="joined", cascade="all, delete-orphan")
    results: Mapped["Result"] = relationship("Result", back_populates="quiz", lazy="selectin")

class Question(Base):
    __tablename__ = "questions"
    quiz_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable = False)
    title:Mapped[str] = mapped_column(String(200), nullable=False)
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions", lazy="selectin")
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="question", lazy="joined", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    question_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"),nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question: Mapped["Question"] = relationship("Question", back_populates="answers", lazy="joined")

class Result(Base):
    __tablename__ = "results"
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    score_percentage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user:Mapped["User"] = relationship("User", back_populates="results", lazy="selectin")
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="results", lazy="selectin")
