# app/schemas/homework.py

from pydantic import BaseModel, constr, conint
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

class HomeworkTypeUpdateRequest(BaseModel):
    name: constr(min_length=1)
    description: str | None = None
    repeat_type: constr(min_length=1)
    repeat_count: conint(ge=1)

class HomeworkTypeDetailResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    reset_type: str
    reset_time: time
    clear_count: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class HomeworkTypeOrderUpdate(BaseModel):
    id: int
    order: int