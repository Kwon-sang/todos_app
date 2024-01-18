from fastapi import HTTPException

from src.todos.models import Todo


async def get_todo_by_id(db, todo_id) -> Todo:
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} is not found.")
    return todo
