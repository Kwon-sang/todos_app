from typing import AsyncGenerator

import pytest
from sqlmodel import SQLModel
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import get_db
from src.main import app

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(url=DATABASE_URL, connect_args={"check_same_thread": False})
SessionTest = sessionmaker(bind=engine, expire_on_commit=False)


def get_test_db():
    with SessionTest() as session:
        yield session


@pytest.fixture(scope="session")
def anyio_backend():
    app.dependency_overrides[get_db] = get_test_db
    return 'asyncio'


@pytest.fixture(autouse=True)
async def db():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    yield


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def create_user(client: AsyncClient) -> None:
    """
    토큰 생성 테스트를 위한 유저 데이터 생성 Fixture
    """
    user_create_request_body = {
        "email": "test@google.com",
        "username": "testuser",
        "password": "1234",
        "first_name": "test",
        "last_name": "user"
    }
    await client.post(url="/users", json=user_create_request_body)
