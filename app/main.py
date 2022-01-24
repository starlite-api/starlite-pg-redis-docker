import asyncio
import logging
from typing import Any

from starlite import OpenAPIConfig, Starlite, get
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from app.api import v1_router

logger = logging.getLogger(__name__)


async def startup(*args: Any, **kwargs: Any) -> None:
    from app.core.database import connect_db
    from app.core.logging import configure_logging
    from app.core.redis import connect_redis
    from app.core.uvloop import configure_uvloop

    configure_logging()
    logger.info("Starting up")

    await asyncio.gather(
        *[
            asyncio.create_task(connect_db()),
            asyncio.create_task(connect_redis()),
            asyncio.create_task(configure_uvloop()),
        ]
    )


async def shutdown(*args: Any, **kwargs: Any) -> None:
    """
    Shutdown calls shared by worker and FastAPI app.
    """
    logger.info("Shutting down")
    from app.core.database import disconnect_db
    from app.core.redis import disconnect_redis

    await asyncio.gather(
        *[
            asyncio.create_task(disconnect_redis()),
            asyncio.create_task(disconnect_db()),
        ]
    )


@get(path="/")
def health_check() -> dict:
    return {"status": "healthy"}


app = Starlite(
    route_handlers=[health_check, v1_router],
    plugins=[SQLAlchemyPlugin()],
    on_startup=[startup],
    on_shutdown=[shutdown],
    openapi_config=OpenAPIConfig(title="Starlite Postgres Example API", version="1.0.0"),
)
