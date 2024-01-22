from typing import Annotated

from fastapi import APIRouter, HTTPException, Body

from src.auth.service import AuthDependency
from src.database import DBDependency
from src.users.models import User, UserRole
from src.todos.models import Todo

router = APIRouter(prefix="/admin", tags=["Admin APIs"])


def validate_role_admin(user_role):
    if user_role != UserRole.ADMIN:
        raise HTTPException(status_code=401, detail="This Operation allowed only for Administer")


@router.get("/todos", status_code=200)
async def retrieve_all_todo(db: DBDependency, auth: AuthDependency) -> list[Todo]:
    validate_role_admin(auth.role)
    return db.query(Todo).all()


@router.get("/users", status_code=200)
async def retrieve_all_user(db: DBDependency, auth: AuthDependency) -> list[User]:
    validate_role_admin(auth.role)
    return db.query(User).all()


@router.patch("/users/{user_id}/role", status_code=204)
async def change_user_role(db: DBDependency, auth: AuthDependency,
                           user_id: int,
                           role: Annotated[UserRole, Body(embed=True)]):
    validate_role_admin(auth.role)
    db.query(User).filter(User.id == user_id).update({"role": role})
    db.commit()


@router.patch("/users/{user_id}/active", status_code=204)
async def change_user_activation_state(db: DBDependency, auth: AuthDependency,
                                       user_id: int,
                                       is_active: Annotated[bool, Body(embed=True)]):
    validate_role_admin(auth.role)
    db.query(User).filter(User.id == user_id).update({"is_active": is_active})
    db.commit()
