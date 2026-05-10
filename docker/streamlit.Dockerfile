# MedXAI Streamlit image — Phase 0 placeholder.
# Same structure as the API image so behaviour is symmetric.

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# LICENSE is required by hatchling at sync time (see pyproject.toml).
COPY pyproject.toml uv.lock README.md LICENSE ./
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
