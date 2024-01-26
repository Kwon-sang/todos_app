from typing import Annotated

from fastapi import APIRouter, HTTPException, Body

from src.auth.service import AuthDependency
from src.users.models import User
from src.todos.models import Todo
from src.database import DB

router = APIRouter(prefix="/admin", tags=["Admin APIs"])


def validate_role_admin(user_role):
    if user_role != "admin":
        raise HTTPException(status_code=401, detail="This Operation allowed only for Administer")


@router.get("/todos", status_code=200)
async def retrieve_all_todo(auth: AuthDependency) -> list[Todo]:
    validate_role_admin(auth.role)
    return await DB.retrieve_all(Todo)


@router.get("/users", status_code=200)
async def retrieve_all_user(auth: AuthDependency) -> list[User]:
    validate_role_admin(auth.role)
    return await DB.retrieve_all(User)


@router.patch("/users/{user_id}/role", status_code=204)
async def change_user_role(auth: AuthDependency,
                           user_id: int,
                           role: Annotated[str, Body(embed=True)]):
    validate_role_admin(auth.role)
    await DB.patch(User, target={"role": role}, id=user_id)


@router.patch("/users/{user_id}/active", status_code=204)
async def change_user_activation_state(auth: AuthDependency,
                                       user_id: int,
                                       is_active: Annotated[bool, Body(embed=True)]):
    validate_role_admin(auth.role)
    await DB.patch(User, target={"is_active": is_active}, id=user_id)
