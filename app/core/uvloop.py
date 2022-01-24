import logging

logger = logging.getLogger(__name__)


async def configure_uvloop() -> None:
    """
    Replace the asyncio event loop with uvloop.

    Uvloop is just a faster drop-in replacement. See docs for more info:
    https://uvloop.readthedocs.io/user/index.html
    """
    logger.info("Setting uvloop event loop policy")
    import asyncio

    from uvloop import EventLoopPolicy

    asyncio.set_event_loop_policy(EventLoopPolicy())
