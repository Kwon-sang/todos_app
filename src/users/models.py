import enum
from typing import Optional, Any

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool = Field(default=True)
    role: str = Field(default="user")

    def __init__(self, **data: Any) -> None:
        if "password" in data:
            password = data.pop("password")
            data["hashed_password"] = self.hash_password(password)
        super().__init__(**data)

    def hash_password(self, password) -> str:
        return bcrypt_context.hash(password)

    def verify_password(self, plain_password):
        return bcrypt_context.verify(plain_password, self.hashed_password)
