from typing import Annotated

from fastapi import APIRouter, Path

from .models import Todo
from .schemas import TodoCreate, TodoUpdate
from src.auth.service import AuthDependency

from src.database import DB

router = APIRouter(prefix="/todos", tags=["Todos APIs"])


@router.get("", status_code=200)
async def retrieve_all(auth: AuthDependency) -> list[Todo]:
    return DB.retrieve_all(Todo, owner_id=auth.user_id)


@router.post("", status_code=201)
async def create_todo(auth: AuthDependency,
                      body: TodoCreate) -> Todo:
    return DB.create(Todo, body, owner_id=auth.user_id)


@router.get("/{todo_id}", status_code=200)
async def retrieve_todo(auth: AuthDependency,
                        todo_id: Annotated[int, Path(gt=0)]):
    return DB.retrieve_one(Todo, id=todo_id, owner_id=auth.user_id)


@router.put("/{todo_id}", status_code=204)
async def update_todo(auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)],
                      body: TodoUpdate) -> None:
    DB.update(Todo, body, id=todo_id, owner_id=auth.user_id)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)]) -> None:
    DB.delete(Todo, id=todo_id, owner_id=auth.user_id)
