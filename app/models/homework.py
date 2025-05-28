from sqlalchemy import Column, Integer, String, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import time, datetime

from app.core.config import Base

class HomeworkType(Base):
    __tablename__ = "homework_types"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String)
    reset_type = Column(String(20), nullable=False)
    reset_time = Column(Time, nullable=False, default=datetime.strptime("06:00", "%H:%M").time())
    clear_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="homework_types")
    assigned_characters = relationship("CharacterHomework", back_populates="homework_type", cascade="all, delete")

    order = Column(Integer, default=0)
