from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Body

from src.database import DBDep
from src.todos.models import Todo
from src.todos.schemas import TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["TODOS"])


async def find_by_id(db, todo_id) -> Todo:
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found.")
    return todo


@router.get("")
async def read_all(db: DBDep) -> list[Todo]:
    return db.query(Todo).all()


@router.post("", status_code=201)
async def create_todo(db: DBDep, body: TodoCreate) -> Todo:
    new_todo = Todo(**body.model_dump())
    db.add(new_todo)
    db.commit()
    return new_todo


@router.get("/{todo_id}")
async def read_todo(db: DBDep,
                    todo_id: Annotated[int, Path(gt=0)]) -> Todo:
    return await find_by_id(db, todo_id)


@router.put("/{todo_id}", status_code=204)
async def update_todo(db: DBDep,
                      todo_id: Annotated[int, Path(gt=0)],
                      body: TodoUpdate) -> None:
    todo = await find_by_id(db, todo_id)
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(db: DBDep,
                      todo_id: Annotated[int, Path(gt=0)]) -> None:
    todo = await find_by_id(db, todo_id)
    db.delete(todo)
    db.commit()
