from typing import Generator, Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from .settings import setting

engine = create_engine(url=setting.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


def filtering_condition_creator(model, **kwargs) -> list[Any]:
    """
    키워드 인자를 filter 인자로 사용할 수 있게 변환하는 함수 입니다.
    eval을 통해 평가된 조건 인자를 리스트에 저장하여 반환합니다.
    ex)
    filtering = filtering_condition_creator(User, id=1, username="kim")
    filtering -> [eval(User.id == 1), eval(User.username == "kim")]
    Session.query(User).filter(*filtering) -> Session.query(User).filter(User.id == 1, User.username == "kim")
    """
    conditions = []
    for key, value in kwargs.items():
        if key not in model.model_fields:
            raise KeyError(f"Field name {key!r} is not found in {model.__name__}")
        conditions.append(eval(f"model.{key} == {value!r}"))
    return conditions


class DB:
    @classmethod
    def retrieve_all(cls, model, /, **kwargs) -> list[Any]:
        db: Session = next(get_db())
        # If not exist filtering condition, Do retrieve all
        if not kwargs:
            return db.query(model).all()
        # Else, Do retrieve with filtering conditions
        else:
            conditions = filtering_condition_creator(model, **kwargs)
            return db.query(model).filter(*conditions).all()

    @classmethod
    def retrieve_one(cls, model, /, **kwargs) -> Any:
        db: Session = next(get_db())
        # At least one filtering option required
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_condition_creator(model, **kwargs)
        result = db.query(model).filter(*conditions).first()
        if not result:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with {kwargs} is not found")
        return result

    @classmethod
    def create(cls, model, body: BaseModel, /,  **kwargs) -> Any:
        db: Session = next(get_db())
        new_model = model(**body.model_dump(), **kwargs)
        db.add(new_model)
        db.commit()
        return new_model

    @classmethod
    def update(cls, model, body: BaseModel, /,  **kwargs) -> None:
        db: Session = next(get_db())
        # At least one filtering option required
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_condition_creator(model, **kwargs)
        row_count = db.query(model).filter(*conditions).update(body.model_dump(exclude_unset=True))
        if row_count == 0:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with {kwargs} is not found")
        db.commit()

    @classmethod
    def patch(cls, model, target: dict, **kwargs) -> None:
        db: Session = next(get_db())
        # At least one filtering option required
        if not kwargs:
            raise ValueError("Filtering option required")
        conditions = filtering_condition_creator(model, **kwargs)
        row_count = db.query(model).filter(*conditions).update(target)
        if row_count == 0:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with {kwargs} is not found")
        db.commit()

    @classmethod
    def delete(cls, model, /, **kwargs) -> None:
        db: Session = next(get_db())
        conditions = filtering_condition_creator(model, **kwargs)
        db.query(model).filter(*conditions).delete()
        db.commit()
