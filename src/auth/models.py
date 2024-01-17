from typing import Optional

from sqlmodel import SQLModel, Field


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