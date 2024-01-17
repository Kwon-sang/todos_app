from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)
    password: str
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

    def hash_password(self):
        pass