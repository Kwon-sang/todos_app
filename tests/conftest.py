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


# Data Configurations
@pytest.fixture
async def create_user(client: AsyncClient) -> dict:
    """
    테스트를 위한 기본 유저를 DB에 생성합니다.
    """
    user_create_request_body = {
        "email": "test@google.com",
        "username": "testuser",
        "password": "1234",
        "first_name": "test",
        "last_name": "user"
    }
    response = await client.post(url="/users", json=user_create_request_body)
    return response.json()


@pytest.fixture
async def issue_token(client: AsyncClient, create_user) -> dict:
    """
    유저 정보를 바탕으로 생성된 토큰을 발행합니다.
    """
    data = {
        "username": "testuser",
        "password": "1234"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await client.post(url="/auth", data=data, headers=headers)
    return response.json()


@pytest.fixture
async def create_todo(client: AsyncClient, create_user, issue_token) -> dict:
    request_body = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': 1}
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    response = await client.post(url="/todos", json=request_body, headers=header)
    return response.json()

