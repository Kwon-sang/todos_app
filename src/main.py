from fastapi import FastAPI

from .models import SQLModel
from .database import engine

app = FastAPI()


@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(bind=engine)