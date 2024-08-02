from uuid import UUID
from pydantic import BaseModel

from app.entity.enums import ActionStatus

class ActionDetail(BaseModel):
    id: UUID
    user_id: UUID
    company_id: UUID
    status: ActionStatus

    class Config:
        from_attributes = True