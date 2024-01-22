from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Claim(BaseModel):
    sub: str
    user_id: int
    role: str
    exp: datetime
