from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class CompanySchema(BaseModel):
    name: str = Field(min_length=5, max_length=200)
    description: str
    is_visible: bool = True

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=5)
    is_visible: Optional[bool] = True

class CompanyDetail(BaseModel):
    id: UUID
    name:str
    description:str
    is_visible:bool

    class Config:
        from_attributes = True
