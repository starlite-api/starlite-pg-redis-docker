from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aioredis import Redis
    from databases import Database

# These are both set to the correct type on startup

# Ignoring the mypy error here seems sensible, since we'd
# otherwise have to check for optionality every time we use them.
# In practice, we "know" they will be set.

database: "Database" = None
redis: "Redis" = None
