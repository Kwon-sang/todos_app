from datetime import timedelta, datetime
from typing import Annotated, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from . import settings, schemas
from ..users.models import User
from src.database import DB

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


async def authenticate_user(username: str, password: str) -> Any:
    user = await DB.retrieve_one(User,
                                 username=username)
    if user.verify_password(password):
        return user
    raise HTTPException(status_code=401, detail="Fail Authentication. Confirm information again.")


def create_access_token(user_id: int, username: str, role: str,  expired_delta: timedelta) -> str:
    expires = datetime.utcnow() + expired_delta
    claim = schemas.Claim(sub=username,
                          user_id=user_id,
                          role=role,
                          exp=expires)
    return jwt.encode(claims=claim.model_dump(),
                      key=settings.JWT_SECRET_KET,
                      algorithm=settings.JWT_ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> schemas.Claim:
    try:
        payload = jwt.decode(token=token,
                             key=settings.JWT_SECRET_KET,
                             algorithms=[settings.JWT_ALGORITHM])
        return schemas.Claim(**payload)
    except JWTError:
        raise HTTPException(status_code=401,
                            detail="Signature invalid",
                            headers={"WWW-Authenticate": "Bearer"})


AuthDependency = Annotated[schemas.Claim, Depends(get_current_user)]
