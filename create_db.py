# create_db.py

from app.core.database import Base, engine
from app.models.user import User
from app.models.character import Character
from app.models.homework import HomeworkType
from app.models.character import CharacterHomework

print("📦 DB 테이블 생성 중...")
Base.metadata.create_all(bind=engine)
print("✅ 완료: sukjenogi.db에 테이블 생성됨.")

