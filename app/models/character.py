from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.config import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    server = Column(String(50))
    job = Column(String(50))
    combat_power = Column(Integer)  # ← 추가된 필드
    auto_synced_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="characters")
    homeworks = relationship("CharacterHomework", back_populates="character", cascade="all, delete")

    order = Column(Integer, default=0)

    is_public = Column(Boolean, default=False, nullable=False)


class CharacterHomework(Base):
    __tablename__ = "character_homeworks"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    homework_type_id = Column(Integer, ForeignKey("homework_types.id", ondelete="CASCADE"), nullable=False)  # ✅ 중요!!

    is_done = Column(Boolean, default=False)
    last_completed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    complete_cnt = Column(Integer, nullable=False, default=0)

    character = relationship("Character", back_populates="homeworks")
    homework_type = relationship("HomeworkType", back_populates="assigned_characters")