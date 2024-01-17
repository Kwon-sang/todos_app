from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Column, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool
    role: str = Field(default="user")


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int
    complete: bool = Field(default=False)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")