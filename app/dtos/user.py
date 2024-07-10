from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class UserSingIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3, max_length=50)
    confirmed_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    current_password: Optional[str] = Field(None, min_length=8)
    new_password: Optional[str] = Field(None, min_length=8)
    confirm_new_password: Optional[str] = None

    @field_validator("confirm_new_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ("passwords do not match")
        return v


class UserDetail(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    create_at: datetime
    update_at: Optional[datetime] = None

    class Config:
        from_attributes = True

