# app/api/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.models.user import User
from app.core.database import SessionLocal
from app.core.deps import get_current_user

router = APIRouter()

# DB 세션 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_create)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
