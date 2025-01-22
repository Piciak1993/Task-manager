from pydantic import BaseModel
from datetime import datetime

class Notification(BaseModel):
    user_id: int
    task_id: int
    action: str
    timestamp: datetime
