# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# 사용자 생성 요청용 (회원가입)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 사용자 응답용
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
