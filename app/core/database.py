import logging

import sqlalchemy
from databases import Database

from app.core import state
from app.core.config import settings

logger = logging.getLogger(__name__)

url = settings.DATABASE_URL.replace(scheme="postgresql")

metadata = sqlalchemy.MetaData()


async def connect_db() -> None:
    if not state.database:
        if not settings.TESTING:
            state.database = Database(url=url)
        else:
            # Roll back the test database to a clean state between each test case
            state.database = Database(url=url, force_rollback=True)

    if not state.database.is_connected:
        logger.info("Connecting to database.")
        await state.database.connect()


async def disconnect_db() -> None:
    if state.database.is_connected:
        logger.info("Disconnecting from database.")
        await state.database.disconnect()
