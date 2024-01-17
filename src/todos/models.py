from typing import Optional

from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int
    complete: bool = Field(default=False)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")