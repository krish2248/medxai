# Changelog

All notable changes to MedXAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

(no work in progress)

## [0.0.1-phase0] — 2026-05-10

### Phase 0 — Scaffolding

- Repo initialised under MIT license with `.gitignore`, `.gitattributes`, `CITATION.cff`.
- README skeleton with the standard disclaimer, status table, and quickstart placeholders.
- `pyproject.toml` with Python 3.11 pinned, `ruff`/`mypy --strict`/`pytest` configured, `uv.lock` committed.
- `dependency-groups.dev` populated; runtime deps kept minimal in Phase 0.
- Pre-commit config: ruff, mypy, end-of-file-fixer, trailing-whitespace, check-yaml/toml/json, detect-secrets, nbstripout.
- `src/medxai/` package with `__version__` and `py.typed` marker.
- Cross-platform `Makefile` + `make.ps1` (POSIX/PowerShell parity). ADR 0001.
- Decision records for cross-platform make, deferred Next.js scaffold, no W&B/Dagshub, deferred DVC/HF Hub, ratcheting coverage floor (ADRs 0001–0005).
- Test scaffold (`tests/{unit,integration,property,e2e,visual}/`) with `conftest.py` and three version-stamp tests.
- Locked white theme: `streamlit_app/.streamlit/config.toml` + `frontend/tailwind.config.ts` + `frontend/app/globals.css`.
- Theme linter (`scripts/lint_theme.py`) with 11 unit tests — fails CI on `bg-black`, `bg-zinc-900`, `dark:` utilities, and Tailwind `darkMode` config.
- Wellness Atlas linter (`scripts/lint_wellness.py`) with 11 unit tests — enforces ≥2 citations and the verbatim disclaimer per article.
- GitHub Actions CI: ruff, ruff-format, mypy, pytest with coverage XML upload, theme + wellness linters, Docker build (gated on Phase-0 Dockerfiles existing).
- MkDocs Material skeleton with index, getting-started, architecture pages and the ADR index.
- Phase-0 Dockerfiles (`docker/api.Dockerfile`, `docker/streamlit.Dockerfile`) + `docker-compose.yml` (api, streamlit, optional jupyter profile).
- `CONTRIBUTING.md`, `SECURITY.md`, `.env.example`, `SESSION_LOG.md` for ongoing work tracking.

### Fixed

- Docker build: `LICENSE` now copied into the builder stage so hatchling can validate `pyproject.toml`'s `license = { file = "LICENSE" }`. Builder switched to `ghcr.io/astral-sh/uv:python3.11-bookworm-slim` for a known-good uv binary.

[Unreleased]: https://github.com/krish2248/medxai/compare/v0.0.1-phase0...HEAD
[0.0.1-phase0]: https://github.com/krish2248/medxai/releases/tag/v0.0.1-phase0
