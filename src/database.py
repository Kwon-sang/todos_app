from typing import Generator, Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(url=DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


def filtering_helper(model, **kwargs):
    conditions = []
    for key, value in kwargs.items():
        conditions.append(eval(f"model.{key} == {value}"))
    return conditions


class DB:
    @classmethod
    async def retrieve_all(cls, model, **kwargs):
        db: Session = next(get_db())
        if not kwargs:
            return db.query(model).all()
        else:
            conditions = filtering_helper(model, **kwargs)
            return db.query(model).filter(*conditions).all()

    @classmethod
    async def retrieve_one(cls, model, **kwargs):
        db: Session = next(get_db())
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_helper(model, **kwargs)
        return db.query(model).filter(*conditions).first()

    @classmethod
    async def create(cls, model, body: BaseModel, **kwargs):
        db: Session = next(get_db())
        new_model = model(**body.model_dump(), **kwargs)
        db.add(new_model)
        db.commit()
        return new_model

    @classmethod
    async def update(cls, model, body: BaseModel, **kwargs) -> int:
        db: Session = next(get_db())
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_helper(model, **kwargs)
        row_count: int = db.query(model).filter(*conditions).update(body.model_dump(exclude_unset=True))
        db.commit()
        return row_count

    @classmethod
    async def patch(cls, model, target: dict, **kwargs):
        db: Session = next(get_db())
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_helper(model, **kwargs)
        row_count: int = db.query(model).filter(*conditions).update(target)
        db.commit()

    @classmethod
    async def delete(cls, model, **kwargs) -> None:
        db: Session = next(get_db())
        if not kwargs:
            raise ValueError("Filtering option required")
        instance = await cls.retrieve_one(model, **kwargs)
        db.delete(instance)
        db.commit()
