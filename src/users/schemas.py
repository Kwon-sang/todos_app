from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)
    password: str
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class UserInfo(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserInfoUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: str = Field(default=None, max_length=50)
    last_name: str = Field(default=None, max_length=50)


class UserPasswordChange(BaseModel):
    password: str
    new_password1: str
    new_password2: str
