from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.entity.base_models import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
