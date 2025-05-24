# app/schemas/homework.py

from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class HomeworkTypeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reset_type: str
    reset_time: Optional[time] = None
    clear_count: Optional[int] = 0

class HomeworkTypeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    reset_type: str
    reset_time: time
    clear_count: int
    created_at: datetime

    class Config:
        orm_mode = True

class HomeworkSelectableResponse(BaseModel):
    homework_id: int
    title: str
    assigned: str  # 'Y' or 'N'
    reset_type: str
    clear_count: int