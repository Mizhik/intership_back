from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AnalyticResponse(BaseModel):
    last_attempt: datetime
    average_score: float
    score_percentage: int

class AnalyticResponseUser(BaseModel):
    user_id: UUID
    quiz_id: UUID
    last_attempt: datetime
