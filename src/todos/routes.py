from typing import Annotated

from fastapi import APIRouter, Path, HTTPException

from .models import Todo
from .schemas import TodoCreate, TodoUpdate
from src.auth.service import AuthDependency

from src.database import DB

router = APIRouter(prefix="/todos", tags=["Todos APIs"])


@router.get("", status_code=200)
async def retrieve_all(auth: AuthDependency) -> list[Todo]:
    return await DB.retrieve_all(Todo, owner_id=auth.user_id)


@router.post("", status_code=201)
async def create_todo(auth: AuthDependency,
                      body: TodoCreate) -> Todo:
    return await DB.create(Todo, body=body, owner_id=auth.user_id)


@router.get("/{todo_id}", status_code=200)
async def retrieve_todo(auth: AuthDependency,
                        todo_id: Annotated[int, Path(gt=0)]):
    todo = await DB.retrieve_one(Todo, id=todo_id, owner_id=auth.user_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item with ID {todo_id} is not found")
    return todo


@router.put("/{todo_id}", status_code=204)
async def update_todo(auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)],
                      body: TodoUpdate) -> None:
    row_count = await DB.update(Todo, body, id=todo_id, owner_id=auth.user_id)
    if not row_count:
        raise HTTPException(status_code=404, detail=f"Todo item with ID {todo_id}is not found")


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)]) -> None:
    await DB.delete(Todo, id=todo_id, owner_id=auth.user_id)
