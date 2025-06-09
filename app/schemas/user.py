# app/schemas/user.py

from pydantic import BaseModel, EmailStr, constr
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

class PasswordUpdateRequest(BaseModel):
    current_password: constr(min_length=4)
    new_password: constr(min_length=6)

    class Config:
        orm_mode = True


class UserPublicInfoResponse(BaseModel):
    id: int
    email: str
    is_friend: bool
    request_sent: bool
    request_received: bool

class UserByCharacterResponse(BaseModel):
    user_id: int
    email: str
    character_id: int
    character_name: str
    server: str
    is_public: bool