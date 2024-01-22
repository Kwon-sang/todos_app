from typing import Annotated

from fastapi import APIRouter, Path, HTTPException

from .models import Todo
from .schemas import TodoCreate, TodoUpdate
from src.database import DBDependency
from src.auth.service import AuthDependency

router = APIRouter(prefix="/todos", tags=["Todos APIs"])


@router.get("", status_code=200)
async def retrieve_all(db: DBDependency,
                       auth: AuthDependency) -> list[Todo]:
    return db.query(Todo).filter(Todo.owner_id == auth.user_id).all()


@router.post("", status_code=201)
async def create_todo(db: DBDependency,
                      auth: AuthDependency,
                      body: TodoCreate) -> Todo:
    new_todo = Todo(owner_id=auth.user_id, **body.model_dump())
    db.add(new_todo)
    db.commit()
    return new_todo


@router.get("/{todo_id}", status_code=200)
async def retrieve_todo(db: DBDependency,
                        auth: AuthDependency,
                        todo_id: Annotated[int, Path(gt=0)]) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id,
                                 Todo.owner_id == auth.user_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo item is not found")


@router.put("/{todo_id}", status_code=204)
async def update_todo(db: DBDependency,
                      auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)],
                      body: TodoUpdate) -> None:
    if (db.query(Todo).
            filter(Todo.id == todo_id, Todo.owner_id == auth.user_id).
            update(body.model_dump(exclude_unset=True))):
        return db.commit()
    raise HTTPException(status_code=404, detail="Todo item is not found")


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(db: DBDependency,
                      auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)]) -> None:
    if (db.query(Todo).
            filter(Todo.id == todo_id, Todo.owner_id == auth.user_id).
            delete()):
        return db.commit()
    raise HTTPException(status_code=404, detail="Todo item is not found")
