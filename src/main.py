from fastapi import FastAPI
from sqlmodel import SQLModel

from src.database import engine
from src.auth.routes import router as auth_router
from src.todos.routes import router as todo_router
from src.users.routes import router as user_router
from src.admin.routes import router as admin_router

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="TODOS Application APIs")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)
app.include_router(admin_router)
