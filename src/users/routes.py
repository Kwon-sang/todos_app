from typing import Annotated

from fastapi import APIRouter, Path, HTTPException

from . import service
from .models import User
from .schemas import UserInfo, UserInfoUpdate, UserCreate, UserPasswordChange
from src.auth.service import AuthDependency

from src.database import DB

router = APIRouter(prefix='/users', tags=["User APIs"])


@router.post("", status_code=201)
async def create_user(body: UserCreate) -> User:
    return await DB.create(User, body)


@router.get("/{user_id}", status_code=200)
async def retrieve_user_info(auth: AuthDependency,
                             user_id: Annotated[int, Path(gt=0)]) -> UserInfo:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Retrieve user info
    user = await DB.retrieve_one(User, id=auth.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User is not found")
    return user


@router.patch("/{user_id}/password", status_code=204)
async def change_password(auth: AuthDependency,
                          user_id: Annotated[int, Path(gt=0)],
                          body: UserPasswordChange) -> None:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Validate correspondence between new passwords
    if body.new_password1 != body.new_password2:
        raise HTTPException(status_code=400, detail="Confirm new-password again")
    # Retrieve User by ID
    user = await DB.retrieve_one(User, id=user_id)
    # Validate between User's origin password and input password
    if not user.verify_password(body.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    # Change password(applied password hashing)
    hashed_password = user.hash_password(body.new_password2)
    await DB.patch(User, target={"hashed_password": hashed_password}, id=user_id)


@router.put("/{user_id}", status_code=204)
async def change_user_info(auth: AuthDependency,
                           user_id: Annotated[int, Path(gt=0)],
                           body: UserInfoUpdate) -> None:
    # Verification of authority accessing a resource
    service.verify_current_user(auth.user_id, user_id)
    # Update user's info
    row_count = await DB.update(User, body=body, id=user_id)
    if not row_count:
        raise HTTPException(status_code=404, detail="User is not found")
