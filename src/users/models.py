import enum
from typing import Optional, Any

from passlib.context import CryptContext
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

    def __repr__(self):
        return self.value


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER)

    def __init__(self, **data: Any) -> None:
        if "password" in data:
            password = data.pop("password")
            data["hashed_password"] = bcrypt_context.hash(password)
        super().__init__(**data)

    def change_password(self, new_password) -> None:
        hashed_password = bcrypt_context.hash(new_password)
        setattr(self, "hashed_password", hashed_password)

    def verify_password(self, plain_password):
        return bcrypt_context.verify(plain_password, self.hashed_password)
