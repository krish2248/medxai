# MedXAI FastAPI image — Phase 0 placeholder.
# The real backend lands in Phase 7. This image is structured exactly as
# the production image will be so the docker-compose surface and the CI
# build step are stable from day one.

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv from the official binary release.
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev --all-extras

# --- Runtime image ---
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Non-root runtime user.
RUN groupadd --system app && useradd --system --gid app --create-home app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src
COPY --from=builder --chown=app:app /app/pyproject.toml /app/README.md /app/

USER app

EXPOSE 8000

# Phase 7 will replace this with the real uvicorn entrypoint:
#   CMD ["uvicorn", "medxai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-c", "import medxai; print(f'medxai {medxai.__version__} — FastAPI lands in Phase 7')"]
