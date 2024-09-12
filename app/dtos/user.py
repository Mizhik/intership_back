from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID



class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3, max_length=50)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDetail(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    create_at: datetime
    update_at: Optional[datetime] = None

    class Config:
        from_attributes = True
