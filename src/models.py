from typing import Optional

from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


