from sqlalchemy import select, case
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.character import CharacterHomework
from app.models.character import Character
from app.models.homework import HomeworkType

def get_homeworks_with_assignment_status(db: Session, user_id: int, character_id: int):
    stmt = (
        select(
            HomeworkType.id.label("homework_id"),
            HomeworkType.title,
            case(
                (CharacterHomework.id != None, 'Y'),
                else_='N'
            ).label("assigned"),
            HomeworkType.reset_type,
            HomeworkType.clear_count
        )
        .outerjoin(
            CharacterHomework,
            (HomeworkType.id == CharacterHomework.homework_type_id) &
            (CharacterHomework.character_id == character_id)
        )
        .where(HomeworkType.user_id == user_id)
        .order_by(HomeworkType.id)
    )

    return db.execute(stmt).mappings().all()

def assign_homework_to_character(db: Session, user_id: int, character_id: int, homework_type_id: int):
    # 캐릭터/숙제 소유자 확인
    character = db.query(Character).filter_by(id=character_id, user_id=user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터가 없습니다.")

    homework = db.query(HomeworkType).filter_by(id=homework_type_id, user_id=user_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="숙제가 없습니다.")

    # 중복 확인
    exists = db.query(CharacterHomework).filter_by(
        character_id=character_id,
        homework_type_id=homework_type_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="이미 지정된 숙제입니다.")

    # INSERT
    ch = CharacterHomework(
        character_id=character_id,
        homework_type_id=homework_type_id
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return {"message": "숙제가 지정되었습니다."}


def unassign_homework_from_character(db: Session, user_id: int, character_id: int, homework_type_id: int):
    # 소유 확인 + 존재 여부
    ch = (
        db.query(CharacterHomework)
        .join(Character)
        .filter(
            Character.id == character_id,
            Character.user_id == user_id,
            CharacterHomework.homework_type_id == homework_type_id
        )
        .first()
    )
    if not ch:
        raise HTTPException(status_code=404, detail="해당 숙제가 지정되어 있지 않습니다.")

    db.delete(ch)
    db.commit()
    return {"message": "숙제가 해제되었습니다."}

def update_homework_completion(
    db: Session,
    user_id: int,
    character_id: int,
    homework_type_id: int,
    new_complete_cnt: int
):
    character = db.query(Character).filter_by(id=character_id, user_id=user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터가 없습니다.")

    homework = db.query(HomeworkType).filter_by(id=homework_type_id, user_id=user_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="숙제를 찾을 수 없습니다.")

    ch = db.query(CharacterHomework).filter_by(
        character_id=character_id,
        homework_type_id=homework_type_id
    ).first()

    if not ch:
        raise HTTPException(status_code=404, detail="지정된 숙제가 없습니다.")

    if new_complete_cnt > homework.clear_count:
        raise HTTPException(status_code=400, detail="완료 횟수가 숙제 클리어 기준을 초과했습니다.")

    # 공통 업데이트
    ch.complete_cnt = new_complete_cnt
    ch.last_completed_at = datetime.utcnow()
    ch.updated_at = datetime.utcnow()

    # 완료 처리
    if new_complete_cnt == homework.clear_count:
        ch.is_done = True
    else:
        ch.is_done = False

    db.commit()
    return {"message": "숙제 완료 상태가 업데이트되었습니다."}

def update_homework_completion(
    db: Session,
    user_id: int,
    character_id: int,
    homework_type_id: int,
    new_complete_cnt: int
):
    character = db.query(Character).filter_by(id=character_id, user_id=user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터가 없습니다.")

    homework = db.query(HomeworkType).filter_by(id=homework_type_id, user_id=user_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="숙제를 찾을 수 없습니다.")

    ch = db.query(CharacterHomework).filter_by(
        character_id=character_id,
        homework_type_id=homework_type_id
    ).first()

    if not ch:
        raise HTTPException(status_code=404, detail="지정된 숙제가 없습니다.")

    if new_complete_cnt > homework.clear_count:
        raise HTTPException(status_code=400, detail="완료 횟수가 숙제 클리어 기준을 초과했습니다.")

    ch.complete_cnt = new_complete_cnt
    ch.last_completed_at = datetime.utcnow()
    ch.updated_at = datetime.utcnow()
    ch.is_done = (new_complete_cnt == homework.clear_count)

    db.commit()
    return {"message": "숙제 완료 상태가 업데이트되었습니다."}