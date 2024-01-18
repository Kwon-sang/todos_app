from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.database import DBDep
from .models import User
from .schemas import UserCreate, Token
from .service import authenticate_user, create_access_token, set_hashed_password_field

router = APIRouter(prefix="/auth", tags=["User Authorization/Authentication"])


@router.post("", status_code=201)
async def create_user(db: DBDep,
                      body: UserCreate) -> User:
    set_hashed_password_field(body)
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    return user


@router.post("/token", status_code=200)
async def login_for_access_token(db: DBDep,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(db=db, username=form_data.username, password=form_data.password)
    token = create_access_token(user_id=user.id, username=user.username, expired_delta=timedelta(minutes=20))
    return Token(token=token, type="bearer")
