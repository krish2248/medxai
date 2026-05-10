# MedXAI Streamlit image — Phase 0 placeholder.
# Same structure as the API image so behaviour is symmetric.

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

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY streamlit_app ./streamlit_app

RUN uv sync --frozen --no-dev --all-extras

# --- Runtime image ---
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --create-home app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src
COPY --from=builder --chown=app:app /app/streamlit_app /app/streamlit_app
COPY --from=builder --chown=app:app /app/pyproject.toml /app/README.md /app/

USER app

EXPOSE 8501

# Phase 2+ will replace this with the real Streamlit entrypoint:
#   CMD ["streamlit", "run", "streamlit_app/Home.py"]
CMD ["python", "-c", "import medxai; print(f'medxai {medxai.__version__} — Streamlit lands in Phase 2')"]
