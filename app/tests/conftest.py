import os
import sys
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.config import settings
from app.database.dependencies import get_session
from app.main import app
from app.tests.clients.user_client import UserClient


engine_test = create_async_engine(
    settings.test_db.url,
    poolclass=NullPool,
)

AsyncSessionTest = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option(
        "sqlalchemy.url", settings.test_db.url.replace("%", "%%")
    )

    command.upgrade(alembic_cfg, "head")
    yield


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine_test.connect() as conn:
        trans = await conn.begin()
        async_session = AsyncSessionTest(bind=conn)

        try:
            yield async_session
        finally:
            await trans.rollback()
            await async_session.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def user_client(client: AsyncClient) -> Generator[UserClient, None, None]:
    yield UserClient(client)
