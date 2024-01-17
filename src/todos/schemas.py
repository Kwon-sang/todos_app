from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    priority: int = Field(gt=0, lt=6)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)
    priority: Optional[int] = Field(default=None, gt=0, lt=6)
    complete: Optional[bool] = None
