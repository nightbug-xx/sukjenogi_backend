# app/schemas/character.py

from pydantic import BaseModel, constr, conint
from typing import Optional
from datetime import datetime

# 캐릭터 생성 요청용
class CharacterCreate(BaseModel):
    name: str
    server: Optional[str] = None
    job: Optional[str] = None
    combat_power: Optional[int] = None  # ← 추가
    is_public: bool = False

# 캐릭터 응답용
class CharacterResponse(BaseModel):
    id: int
    name: str
    server: Optional[str]
    job: Optional[str]
    combat_power: Optional[int]  # ← 추가
    is_public: bool
    auto_synced_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True

class CharacterUpdateRequest(BaseModel):
    name: constr(min_length=1)
    server: constr(min_length=1)
    power: conint(ge=0)  # 0 이상 정수
    is_public: bool

class CharacterDetailResponse(BaseModel):
    id: int
    name: str
    server: str
    combat_power: int
    user_id: int
    is_public: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class CharacterOrderUpdate(BaseModel):
    id: int
    order: int
