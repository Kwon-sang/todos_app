from fastapi import HTTPException
from sqlmodel import Session

from . import models


async def get_user_by_username(db: Session, username: str) -> models.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with username {username!r} is not found.")
    return user


async def get_user_by_id(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id!r} is not found.")
    return user


def verify_current_user(login_user_id, user_id) -> None:
    if login_user_id != user_id:
        raise HTTPException(status_code=403, detail="No permission")

