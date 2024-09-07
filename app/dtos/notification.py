from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    text:str
    status: bool
    create_at: datetime
    
    class Config:
        from_attributes = True


