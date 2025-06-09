# app/api/user.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.logger import logger
import traceback
import sys
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, PasswordUpdateRequest, UserPublicInfoResponse, UserByCharacterResponse
from app.crud.user import create_user
from app.models.user import User
from app.core.database import SessionLocal
from app.core.deps import get_current_user
from app.core.security import verify_password, get_password_hash
from app.services import user_service

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

@router.put("/me/password", status_code=204)
def update_password(
    pw_req: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if not verify_password(pw_req.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="현재 비밀번호가 일치하지 않습니다."
            )

        print("기존:", current_user.password_hash)
        print("신규:", get_password_hash(pw_req.new_password))

        current_user = db.merge(current_user)  # 세션에 붙임
        current_user.password_hash = get_password_hash(pw_req.new_password)
        db.flush()
        db.expunge(current_user)
        print("✅ flush 완료됨. 커밋 시도 중...")
        db.commit()
        print("✅ 커밋 완료됨.")
    except Exception as e:
        logger.error(f"❌ 비밀번호 변경 중 예외 발생: {e}")
        traceback.print_exc(file=sys.stdout)  # ← 여기가 핵심
        raise

@router.get("/public-info", response_model=UserPublicInfoResponse)
def get_public_info(
        email: str = Query(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return user_service.get_user_public_info(db, current_user.id, email)

@router.get("/by-character", response_model=UserByCharacterResponse)
def get_by_character(
    server: str,
    name: str,
    db: Session = Depends(get_db)
):
    return user_service.get_user_by_character(db, server, name)