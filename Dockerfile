FROM python:3.11.5-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin" \
    IN_DOCKER=true

WORKDIR /usr/local/src/task_manager

RUN apt-get update && apt-get install -y curl make git gettext \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && git config --global --add safe.directory `pwd`

COPY . .
RUN poetry install