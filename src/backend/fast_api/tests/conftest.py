from dotenv import load_dotenv
import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from main import app
from db.config import Base, engine
from typing import Any
from typing import Generator
import json
from db.config import (
    async_session,
    get_session,
    create_async_engine,
    modules,
    sessionmaker,
    AsyncSession,
)
import os

TEST_DATABASE_URL = f"postgresql+asyncpg://{os.getenv('TEST_POSTGRES_USER')}:{os.getenv('TEST_POSTGRES_PASSWORD')}@{os.getenv('TEST_POSTGRES_HOST')}:{os.getenv('TEST_POSTGRES_PORT')}/{os.getenv('TEST_POSTGRES_DB')}"

test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

test_async_session = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_db():
    try:
        db = test_async_session()
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> Generator[AsyncClient, Any, Any]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.dependency_overrides[get_session] = override_db
        """
        Create a fresh database on each test case.
        """
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield client

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
