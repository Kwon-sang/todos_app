from fastapi import APIRouter

from src.schemas import UserCreate
from src.models import User
from src.database import DBDep

router = APIRouter(prefix="/users")


@router.post("", status_code=201)
async def create_user(db: DBDep,
                      body: UserCreate) -> User:
    body.hash_password()
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    return user
