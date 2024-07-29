from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.entity.base_models import Base
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    owned_companies: Mapped[list["Company"]] = relationship("Company", back_populates="owner", lazy='selectin')

class Company(Base):
    __tablename__ = "companies"
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="owned_companies")
