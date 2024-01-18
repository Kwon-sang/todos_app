from datetime import timedelta, datetime
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from .models import User
from .schemas import Claim

JWT_SECRET_KET = "db278fda906fcf6f8bfb93ef4c64a07a7ae6d369b2089a40e5574fa52115899d"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE__MINUTE_DELTA = 20

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def set_hashed_password_field(obj):
    if hasattr(obj, 'password'):
        hashed_password = bcrypt_context.hash(obj.password)
        setattr(obj, "hashed_password", hashed_password)


def verify_user_password(plain_password, encrypted_password) -> bool:
    return bcrypt_context.verify(plain_password, encrypted_password)


async def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with username {username!r} is not found.")
    return user


async def authenticate_user(db: Session, username: str, password: str) -> User:
    user = await get_user_by_username(db, username)
    if not verify_user_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Fail Authentication. Confirm information again.")
    return user


def create_access_token(user_id: int, username: str, expired_delta: timedelta) -> str:
    expires = datetime.utcnow() + expired_delta
    claim = Claim(id=user_id, sub=username, exp=expires)
    return jwt.encode(claims=claim.model_dump(), key=JWT_SECRET_KET, algorithm=JWT_ALGORITHM)


def get_current_user_claim(token: Annotated[str, Depends(oauth2_bearer)]) -> Claim:
    try:
        payload = jwt.decode(token=token, key=JWT_SECRET_KET, algorithms=[JWT_ALGORITHM])
        return Claim(**payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Fail Authentication. Confirm information again.")
