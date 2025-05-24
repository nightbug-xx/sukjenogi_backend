# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, create_access_token
from pydantic import BaseModel, EmailStr
from datetime import timedelta

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 로그인 요청 스키마
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# 로그인 응답 스키마
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60 * 24)  # 1일
    )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/check-email")
def check_email_availability(
    email: str = Query(..., description="중복 확인할 이메일 주소"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    return {"available": user is None}