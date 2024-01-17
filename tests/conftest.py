from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import get_db
from src.main import app
from src import models

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
    models.SQLModel.metadata.drop_all(bind=engine)
    models.SQLModel.metadata.create_all(bind=engine)
    yield


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
