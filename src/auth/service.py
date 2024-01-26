import os
from datetime import timedelta, datetime
from typing import Annotated, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .schemas import Claim
from src.users.models import User
from src.database import DB

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth")
KEY = os.environ["JWT_SECRET_KET"]
ALGORITHM = os.environ["JWT_ALGORITHM"]


async def authenticate_user(username: str, password: str) -> Any:
    user = await DB.retrieve_one(User, username=username)
    # 단순 편의 목적: DB direct SQL을 통해 생성한 암호화 되지 않은 슈퍼유저를 위해
    if user.role == "admin":
        return user
    # encrypted password verification
    if user.verify_password(password):
        return user
    raise HTTPException(status_code=401, detail="Fail Authentication. Confirm information again.")


def create_access_token(user_id: int, username: str, role: str, expired_delta: timedelta) -> str:
    expires = datetime.utcnow() + expired_delta
    claim = Claim(sub=username,
                  user_id=user_id,
                  role=role,
                  exp=expires)
    return jwt.encode(claims=claim.model_dump(), key=KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> Claim:
    try:
        payload = jwt.decode(token=token, key=KEY, algorithms=ALGORITHM)
        return Claim(**payload)
    except JWTError:
        raise HTTPException(status_code=401,
                            detail="Signature invalid",
                            headers={"WWW-Authenticate": "Bearer"})


AuthDependency = Annotated[Claim, Depends(get_current_user)]
