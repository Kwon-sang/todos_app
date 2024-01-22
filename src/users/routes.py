from typing import Annotated

from fastapi import APIRouter, Path, HTTPException

from . import models, schemas
from . import service
from src.database import DBDependency
from src.auth.service import AuthDependency

router = APIRouter(prefix='/users', tags=["User APIs"])


@router.post("", status_code=201)
async def create_user(db: DBDependency,
                      body: schemas.UserCreate) -> models.User:
    user = models.User(**body.model_dump())
    db.add(user)
    db.commit()
    return user


@router.get("/{user_id}", status_code=200)
async def retrieve_user_info(db: DBDependency,
                             auth: AuthDependency,
                             user_id: Annotated[int, Path(gt=0)]) -> schemas.UserInfo:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Retrieve user info
    if user := (db.query(models.User).
                filter(models.User.id == auth.user_id).
                first()):
        return user
    raise HTTPException(status_code=404, detail="User is not found")


@router.patch("/{user_id}/password", status_code=204)
async def change_password(db: DBDependency,
                          auth: AuthDependency,
                          user_id: Annotated[int, Path(gt=0)],
                          body: schemas.UserPasswordChange) -> None:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Validate correspondence between new passwords
    if body.new_password1 != body.new_password2:
        raise HTTPException(status_code=400, detail="Confirm new-password again")
    # Retrieve User by ID
    user = await service.get_user_by_id(db, user_id)
    # Validate between User's origin password and input password
    if not user.verify_password(body.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    # Change password(applied password hashing)
    user.change_password(body.new_password2)
    db.add(user)
    db.commit()


@router.put("/{user_id}", status_code=204)
async def change_user_info(db: DBDependency,
                           auth: AuthDependency,
                           user_id: Annotated[int, Path(gt=0)],
                           body: schemas.UserInfoUpdate) -> None:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Update user's info
    if (db.query(models.User).
            filter(models.User.id == auth.user_id).
            update(body.model_dump(exclude_unset=True))):
        return db.commit()
    raise HTTPException(status_code=404, detail="User is not found")
