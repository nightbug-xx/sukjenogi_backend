from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class FriendRequestStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"

class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(FriendRequestStatus), default=FriendRequestStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 🔽 문자열로 참조
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests")

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id_1 = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id_1", "user_id_2", name="unique_friend_pair"),
        CheckConstraint("user_id_1 < user_id_2", name="check_user_order"),
    )

    user1 = relationship("User", foreign_keys=[user_id_1], back_populates="friendships1")
    user2 = relationship("User", foreign_keys=[user_id_2], back_populates="friendships2")
