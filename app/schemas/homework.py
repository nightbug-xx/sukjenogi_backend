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
    is_public: bool = False

class HomeworkTypeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    reset_type: str
    reset_time: time
    clear_count: int
    is_public: bool
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
    title: constr(min_length=1)
    description: str | None = None
    reset_type: constr(min_length=1)
    clear_count: conint(ge=1)
    is_public: bool

class HomeworkTypeDetailResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    reset_type: str
    reset_time: time
    clear_count: int
    is_public: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class HomeworkTypeOrderUpdate(BaseModel):
    id: int
    order: int