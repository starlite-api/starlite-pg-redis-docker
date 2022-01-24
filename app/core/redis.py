import logging

from aioredis import from_url

from app.core import state
from app.core.config import settings

logger = logging.getLogger(__name__)


async def connect_redis() -> None:
    if state.redis is not None:
        return

    logger.info("Connecting to redis")
    state.redis = await from_url(settings.REDIS_URL)


async def disconnect_redis() -> None:
    logger.info("Disconnecting from redis")
    if state.redis:
        await state.redis.close()
