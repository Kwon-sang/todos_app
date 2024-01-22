from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(url=DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


DBDependency = Annotated[Session, Depends(get_db)]
