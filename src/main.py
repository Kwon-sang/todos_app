from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine
from .routes import todo
from . import models

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="TODOS APIs")
app.include_router(todo.router)
