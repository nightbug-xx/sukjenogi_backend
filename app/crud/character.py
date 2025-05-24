#app/crud/character.py

from sqlalchemy.orm import Session
from app.models.character import Character
from app.schemas.character import CharacterCreate
from datetime import datetime

# 외부 크롤링 모듈 불러오기 (예시)
def fetch_character_stats(name: str, server: str):
    # 실제 크롤링 로직으로 교체 필요
    # 예시: {'job': '전사', 'power': 123456}
    return {
        "job": "(크롤링된 직업)",
        "power": 123456
    }

def create_character(user_id: int, character_data: CharacterCreate, db: Session) -> Character:
    character = Character(
        user_id=user_id,
        name=character_data.name,
        server=character_data.server,
        job=character_data.job,
        combat_power=character_data.combat_power,  # ← 수동 입력 허용
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(character)
    db.commit()
    db.refresh(character)

    # 자동 동기화는 combat_power 없을 때만 시도 (선택사항)
    if character.combat_power is None:
        stats = fetch_character_stats(character.name, character.server)
        # character.job = stats.get("job")
        # character.combat_power = stats.get("power")
        # character.auto_synced_at = datetime.utcnow()
        # db.commit()
        # db.refresh(character)

    return character

def get_characters_by_user(user_id: int, db: Session):
    return db.query(Character).filter(Character.user_id == user_id).all()
