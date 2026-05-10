# MedXAI FastAPI image — Phase 0 placeholder.
# The real backend lands in Phase 7. This image is structured exactly as
# the production image will be so the docker-compose surface and the CI
# build step are stable from day one.

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# License file is referenced by pyproject.toml's `license = { file = "LICENSE" }`
# and must be present at sync time for hatchling to validate metadata.
COPY pyproject.toml uv.lock README.md LICENSE ./
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
