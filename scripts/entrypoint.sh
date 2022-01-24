#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Running entrypoint"

redis_ready() {
    python << END
import asyncio
import sys

from aioredis import Redis


async def c():
    try:
        redis = Redis.from_url("${REDIS_URL}", db=0)
        await redis.ping()
    except ConnectionError:
        sys.exit(-1)


if __name__ == '__main__':
    asyncio.run(c())
END
}

postgres_ready() {
  python <<END
import asyncio
import sys
from asyncpg import connect


async def c():
    database_url = "${DATABASE_URL}".replace('+asyncpg','')
    try:
        await connect(dsn=f"{database_url}")
    except ConnectionRefusedError:
        sys.exit(-1)

if __name__ == '__main__':
    asyncio.run(c())
END
}

# Check Gunicorn config
gunicorn --check-config --config=gunicorn.conf.py app.main:app

# Wait for redis to be ready
until redis_ready; do
  >&2 echo "Waiting for Redis to become available..."
  sleep 5
done
>&2 echo "Redis is available"

# Wait for postgres to be ready
until postgres_ready; do
  echo >&2 "Waiting for PostgreSQL to become available..."
  sleep 5
done
echo >&2 "PostgreSQL is available"

#: Run migrations
alembic upgrade head

exec "$@"
