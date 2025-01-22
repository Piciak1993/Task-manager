from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    hours_to_complete = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
