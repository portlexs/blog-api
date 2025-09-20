import os
import sys

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from config import settings
from database.dependencies import get_session
from database.session import Base
from tests.clients.user_client import UserClient


engine_test = create_async_engine(settings.test_db.url, echo=False)
SessionFactory = async_sessionmaker(bind=engine_test, autoflush=False, autocommit=False)


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine_test.connect() as connection:
        trans = await connection.begin()
        async_session = SessionFactory(bind=connection)

        try:
            yield async_session
        finally:
            await async_session.close()
            await trans.rollback()


async def override_get_session():
    async with SessionFactory() as session:
        yield session


@pytest_asyncio.fixture()
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def user_client(client):
    return UserClient(client)
