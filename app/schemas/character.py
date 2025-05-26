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

# 캐릭터 응답용
class CharacterResponse(BaseModel):
    id: int
    name: str
    server: Optional[str]
    job: Optional[str]
    combat_power: Optional[int]  # ← 추가
    auto_synced_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True

class CharacterUpdateRequest(BaseModel):
    name: constr(min_length=1)
    server: constr(min_length=1)
    power: conint(ge=0)  # 0 이상 정수