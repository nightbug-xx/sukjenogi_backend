from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    from app.models.character import Character
    characters = relationship(Character, back_populates="user")
    homework_types = relationship("HomeworkType", back_populates="user", cascade="all, delete")

    # 🔽 문자열만 사용하고 foreign_keys 생략 (권장)
    sent_requests = relationship("FriendRequest", back_populates="from_user", foreign_keys="FriendRequest.from_user_id")
    received_requests = relationship("FriendRequest", back_populates="to_user", foreign_keys="FriendRequest.to_user_id")
    friendships1 = relationship("Friend", back_populates="user1", foreign_keys="Friend.user_id_1")
    friendships2 = relationship("Friend", back_populates="user2", foreign_keys="Friend.user_id_2")