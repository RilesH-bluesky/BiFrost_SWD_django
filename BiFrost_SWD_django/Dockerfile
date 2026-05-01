# syntax=docker/dockerfile:1

FROM python:3.14-slim-bookworm

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libcairo2 \
    libcairo2-dev \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_CACHE_DIR=/tmp/.uv-cache

RUN mkdir -p /tmp/.uv-cache

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

# Since Dockerfile is INSIDE BiFrost_SWD_django,
# pyproject.toml and uv.lock are in the SAME directory.
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

# Copy the entire Django project (current folder) into /app
COPY . .

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
