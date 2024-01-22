from typing import Annotated

from fastapi import APIRouter, Path, HTTPException

from . import models, schemas
from src.database import DBDependency
from src.auth.service import AuthDependency

router = APIRouter(prefix="/todos", tags=["Todos APIs"])


@router.get("", status_code=200)
async def retrieve_all(db: DBDependency,
                       auth: AuthDependency) -> list[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.owner_id == auth.user_id).all()


@router.post("", status_code=201)
async def create_todo(db: DBDependency,
                      auth: AuthDependency,
                      body: schemas.TodoCreate) -> models.Todo:
    new_todo = models.Todo(owner_id=auth.user_id, **body.model_dump())
    db.add(new_todo)
    db.commit()
    return new_todo


@router.get("/{todo_id}", status_code=200)
async def retrieve_todo(db: DBDependency,
                        auth: AuthDependency,
                        todo_id: Annotated[int, Path(gt=0)]) -> models.Todo:
    todo = db.query(models.Todo.id == todo_id,
                    models.Todo.owner_id == auth.user_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo item is not found")


@router.put("/{todo_id}", status_code=204)
async def update_todo(db: DBDependency,
                      auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)],
                      body: schemas.TodoUpdate) -> None:
    if (db.query(models.Todo).
            filter(models.Todo.id == todo_id, models.Todo.owner_id == auth.user_id).
            update(body.model_dump())):
        return db.commit()
    raise HTTPException(status_code=404, detail="Todo item is not found")


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(db: DBDependency,
                      auth: AuthDependency,
                      todo_id: Annotated[int, Path(gt=0)]) -> None:
    if (db.query(models.Todo).
            filter(models.Todo.id == todo_id, models.Todo.owner_id == auth.user_id).
            delete()):
        return db.commit()
    raise HTTPException(status_code=404, detail="Todo item is not found")
