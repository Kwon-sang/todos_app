from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Claim(BaseModel):
    sub: str
    id: int
    exp: datetime


class Token(BaseModel):
    token: str
    type: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)
    password: str
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

    model_config = ConfigDict(extra='allow',
                              json_schema_extra={
                                  "example": {
                                      "email": "Useremail@google.com",
                                      "username": "Username",
                                      "password": "Users password",
                                      "first_name": "User First Name",
                                      "last_name": "User Last Name"
                                  }
                              })
