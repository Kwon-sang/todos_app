from fastapi import FastAPI
from sqlmodel import SQLModel

from src.database import engine
from src.auth.routes import router as auth_router
from src.todos.routes import router as todo_router

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="TODOS APIs")
app.include_router(todo_router)
app.include_router(auth_router)
