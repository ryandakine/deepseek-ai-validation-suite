# syntax=docker/dockerfile:1

# ===== Base image =====
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . ${APP_HOME}

# ===== Dependencies layer =====
FROM base AS deps

# Install Python deps
RUN python -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .[all]

ENV PATH="/venv/bin:$PATH"

# ===== Runtime image =====
FROM python:3.12-slim AS runtime

ENV APP_HOME=/app \
    PATH="/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

# Copy venv from deps stage
COPY --from=deps /venv /venv

# Copy app
COPY --from=base ${APP_HOME} ${APP_HOME}

# Expose no ports by default; GUI runs locally, CLI tools invoked inside container

# Default command: show help
CMD ["bash", "-lc", "echo 'DeepSeek AI Validation Suite container ready. Run: deepseek-validate or deepseek-gui' && sleep infinity"]
