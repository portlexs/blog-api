import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_async_engine(settings.db.url)
    SessionLocal = async_sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )

    app.state.session_factory = SessionLocal

    yield

    await engine.dispose()
