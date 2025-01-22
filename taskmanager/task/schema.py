from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    hours_to_complete: float
    user_id: int | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    hours_to_complete: float
    user_id: int | None

    class Config:
        orm_mode = True