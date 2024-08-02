from sqlalchemy import Boolean, Enum, ForeignKey, String, Text

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

class Company(Base):
    __tablename__ = "companies"
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    actions: Mapped[list["Action"]] = relationship("Action", back_populates='company', lazy="selectin")

class Action(Base):
    __tablename__ = "actions"
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    status: Mapped[ActionStatus] = mapped_column('status', Enum(ActionStatus), default=None)
    user: Mapped["User"] = relationship("User", back_populates="actions")
    company: Mapped["Company"] = relationship("Company", back_populates="actions",)