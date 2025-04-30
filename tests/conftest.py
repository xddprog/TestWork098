import asyncio
from typing import Generator
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from httpx import AsyncClient
from backend.api.dependency.providers.request import RequestProvider
from backend.infrastructure.database.models.base import Base
import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from backend.main import app
from tests.config import TEST_DB_CONFIG
from tests.dependency import TestAppProvider


engine = create_async_engine(TEST_DB_CONFIG.get_postgres_url(), poolclass=NullPool)



@pytest.fixture(autouse=True, scope="session")
async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=False)
async def async_client():
    async with AsyncClient(base_url="http://localhost:8000/api/v1") as client:
        yield client


@pytest.fixture(autouse=False)
async def db_session():
    session = AsyncSession(bind=engine)
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="session")
def test_container():
    return make_async_container(
        RequestProvider(),
        TestAppProvider(),
        FastapiProvider()
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_dishka(test_container):
    setup_dishka(container=test_container, app=app)
