from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import settings
from .schemas import Token
from .service import authenticate_user, create_access_token
from src.database import DBDependency


router = APIRouter(tags=["Authorization/Authentication APIs"])


@router.post(path=settings.TOKEN_URL, status_code=200)
async def login_for_access_token(db: DBDependency,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(db=db, username=form_data.username, password=form_data.password)
    token: str = create_access_token(user_id=user.id,
                                     username=user.username,
                                     role=user.role,
                                     expired_delta=timedelta(minutes=20))
    return Token(access_token=token, token_type="bearer")
