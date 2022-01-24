import os

os.environ["TESTING"] = "True"
os.environ["ENVIRONMENT"] = "local"

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from starlite import TestClient

from app.core.config import settings
from app.core.database import metadata
from app.core.state import database as database_
from app.main import app

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from starlette.testclient import TestClient


@pytest.fixture
async def _database() -> "AsyncGenerator":
    engine = create_async_engine(str(settings.DATABASE_URL))
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    if not database_.is_connected:
        await database_.connect()
    yield
    if database_.is_connected:
        await database_.disconnect()


@pytest.fixture(scope="function")
def test_client() -> TestClient:
    return TestClient(app=app)
