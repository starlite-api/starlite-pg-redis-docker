from collections.abc import Awaitable
from typing import Any

from redis.asyncio import Redis
from starlite import CacheConfig, Request
from starlite.config import CacheBackendProtocol, default_cache_key_builder

from app.config import app_settings, cache_settings

redis = Redis.from_url(cache_settings.URL)


class RedisAsyncioBackend(CacheBackendProtocol):  # pragma: no cover
    async def get(self, key: str) -> Awaitable[Any]:  # pylint: disable=invalid-overridden-method
        """
        Retrieve a value from cache corresponding to the given key.
        """
        return await redis.get(key)  # type:ignore[return-value]

    async def set(  # pylint: disable=invalid-overridden-method
        self, key: str, value: Any, expiration: int
    ) -> Awaitable[Any]:
        """
        Set a value in cache for a given key with a given expiration in seconds.
        """
        return await redis.set(key, value, expiration)  # type:ignore[return-value]

    async def delete(self, key: str) -> Awaitable[Any]:  # pylint: disable=invalid-overridden-method
        """
        Remove a value from the cache for a given key.
        """
        return await redis.delete(key)  # type:ignore[return-value]


async def on_shutdown() -> None:
    """
    Passed to `Starlite.on_shutdown`.
    """
    await redis.close()


def cache_key_builder(request: Request) -> str:
    """
    Prefixes the default cache key with the app name.

    Parameters
    ----------
    request : Request

    Returns
    -------
    str
    """
    return f"{app_settings.NAME}:{default_cache_key_builder(request)}"


config = CacheConfig(
    backend=RedisAsyncioBackend(),
    expiration=cache_settings.EXPIRATION,
    cache_key_builder=cache_key_builder,
)
