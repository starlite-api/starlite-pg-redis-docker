# Pull base image
FROM python:3.10-slim as base

ARG INSTALL_ARGS="--no-root --no-dev"

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.1.12 \
    PYTHONPATH=/app

# Install Poetry
RUN python3 -m pip install "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false

# Upgrade pip and build tools
RUN pip install pip wheel setuptools --user --upgrade

FROM base as dependencies

COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install $INSTALL_ARGS

# Copy relevant files
COPY ./scripts/entrypoint.sh /app/entrypoint.sh
COPY ./scripts/start.sh /app/start.sh
COPY ./gunicorn.conf.py /app/gunicorn.conf.py
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic/ /app/alembic/
COPY ./app/ /app/app/

RUN chmod +x entrypoint.sh && chmod +x start.sh
RUN useradd -m myuser
USER myuser:myuser

ENTRYPOINT  ["bash", "/app/entrypoint.sh"]

FROM dependencies as web

CMD [ "/app/start.sh", "web" ]

FROM dependencies as worker

CMD [ "/app/start.sh", "worker" ]
