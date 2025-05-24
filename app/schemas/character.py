# app/schemas/character.py

from pydantic import BaseModel
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
