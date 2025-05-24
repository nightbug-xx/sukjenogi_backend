from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.character import Character, CharacterHomework
from app.models.homework import HomeworkType
from app.schemas.dashboard import DashboardCharacter, DashboardHomework


def get_dashboard_characters(db: Session, user_id: int):
    subq = db.query(CharacterHomework.character_id).distinct().subquery()

    rows = (
        db.query(Character.id.label("character_id"), Character.name.label("character_name"), Character.server)
        .join(subq, Character.id == subq.c.character_id)
        .filter(Character.user_id == user_id)
        .order_by(Character.id)
        .all()
    )

    return [
        DashboardCharacter(
            character_id=row[0],
            character_name=row[1],
            server=row[2]
        ) for row in rows
    ]


def get_dashboard_homeworks_for_character(db: Session, user_id: int, character_id: int):
    character = db.query(Character).filter_by(id=character_id, user_id=user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    rows = (
        db.query(
            HomeworkType.id.label("homework_id"),
            HomeworkType.title,
            HomeworkType.reset_type,
            HomeworkType.clear_count,
            CharacterHomework.complete_cnt
        )
        .join(CharacterHomework, CharacterHomework.homework_type_id == HomeworkType.id)
        .filter(CharacterHomework.character_id == character_id)
        .order_by(HomeworkType.id)
        .all()
    )

    return [
        DashboardHomework(
            homework_id=row[0],
            title=row[1],
            reset_type=row[2],
            clear_count=row[3],
            complete_cnt=row[4]
        ) for row in rows
    ]
