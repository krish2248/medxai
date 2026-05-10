# MedXAI — Session Log

> Daily progress journal. Each session appends a date-stamped entry with
> what landed, what was decided, what was deferred, and what's next.
> Not a replacement for `CHANGELOG.md` — this is the human story of how
> the project came together; CHANGELOG is the machine-readable summary.

---

## 2026-05-10 — Phase 0 scaffolding (Session 1)

**Goal of the session.** Read the spec end to end, write the plan,
scaffold the entire repo per Phase 0, and push it live to GitHub.

**Decisions taken (logged as ADRs in `docs/decisions/`):**

| ADR | Decision | Why |
|---|---|---|
| 0001 | Cross-platform Make wrapper (`Makefile` + `make.ps1`) | User is on Windows; avoid mandating WSL |
| 0002 | Defer full Next.js scaffold to Phase 7 | Phase 0 only needs theme tokens; no Node bloat in CI |
| 0003 | Skip W&B and Dagshub in v1 | MLflow local is enough; no third-party accounts to set up |
| 0004 | Defer DVC remote and HF Hub setup | Phase 0 stays credential-free |
| 0005 | Coverage floor ratchets up by phase (0/60/75/80) | Tiny denominators in Phase 0 would let regressions through |

**What landed (commits in order):**

1. `chore(repo)` — `.gitignore`, `.gitattributes`, `LICENSE` (MIT), `CITATION.cff`, the spec file (renamed `MEDXAI_PROMPT (1).md` → `MEDXAI_PROMPT.md`), and `docs/PLAN.md`.
2. `docs(readme)` — README skeleton with the verbatim Section 11.4 disclaimer, status table, and quickstart placeholders.
3. `build(deps)` — `pyproject.toml` (Python 3.11 pinned, ruff/mypy/pytest configured), `uv.lock`, the `medxai` package with `__version__`, `.python-version`.
4. `chore(scaffold)` — `.pre-commit-config.yaml` + `.secrets.baseline` (ruff/mypy/eof/ws/yaml/toml/json/secrets/nbstripout).
5. `build(make)` — `Makefile` + `make.ps1` + the five Phase-0 ADRs.
6. `build(coverage)` — Phase-0 coverage floor lowered from 50 to 0 (only `__init__.py` exists in `src/medxai/`); ADR 0005 amended to match.
7. `test(pkg)` — Test scaffold (`tests/{unit,integration,property,e2e,visual}/`) with `conftest.py` and three version-stamp tests (3 passed).
8. `feat(theme)` — Locked white theme tokens for Streamlit (`.streamlit/config.toml`) and Tailwind/Next.js (`tailwind.config.ts`, `globals.css`).
9. `feat(ci)` — `scripts/lint_theme.py` with 11 unit tests; flags `bg-black`, `bg-zinc-900`, `dark:` utilities, and Tailwind `darkMode` config.
10. `feat(ci)` — `scripts/lint_wellness.py` with 11 unit tests; enforces ≥2 citations and the verbatim disclaimer per article (no-op until Phase 6).
11. `ci(actions)` — `.github/workflows/ci.yml`: ruff, ruff-format, mypy, pytest, theme linter, wellness linter, conditional Docker build, coverage XML upload.
12. `docs(mkdocs)` — MkDocs Material with white theme + `index.md`, `getting_started.md`, `architecture.md`. `mkdocs build --strict` is green.
13. `build(docker)` — Phase-0 `docker/api.Dockerfile`, `docker/streamlit.Dockerfile`, `docker-compose.yml` (api + streamlit + opt-in jupyter profile).
14. `docs(meta)` — `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.env.example`, this file.

**Local verification before push:**

- `uv run ruff check .` — clean
- `uv run ruff format --check .` — clean
- `uv run mypy src/medxai` — `Success: no issues found in 1 source file`
- `uv run pytest -q` — 25 passed, 100% coverage on `src/medxai/__init__.py`
- `uv run python -m scripts.lint_theme` — clean (frontend + streamlit_app)
- `uv run python -m scripts.lint_wellness` — clean (no Phase-6 articles yet)
- `uv run mkdocs build --strict` — green

**Pushed to:** `https://github.com/krish2248/medxai` (created in this session).

**Post-push fixes (CI feedback loop):**

- First push to `main` failed the Docker build job: `hatchling` validates
  `pyproject.toml`'s `license = { file = "LICENSE" }` at `uv sync` time and
  the Dockerfiles only copied `pyproject.toml` + `uv.lock` + `README.md`.
- Fixed on a feature branch `chore/phase-0-wrap`:
  - `COPY ... LICENSE ./` added to both Dockerfiles.
  - Switched the builder stage from `python:3.11-slim` + `COPY --from=ghcr.io/astral-sh/uv:0.5.11`
    to `FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim` (the previous
    pinned uv tag did not exist in the registry).
- PR #1 opened, CI green (lint+test 17 s, docker build 2 m 1 s),
  fast-forward merged into `main`, branch deleted.
- Tagged **v0.0.1-phase0** and published as a GitHub release.

**Final state at end of session:**

- 17 commits on `main` (including the merge commit).
- Tag `v0.0.1-phase0` pushed.
- 1 PR opened and merged.
- CI is green on `main` and on the tagged release.
- Repo URL: <https://github.com/krish2248/medxai>
- Release URL: <https://github.com/krish2248/medxai/releases/tag/v0.0.1-phase0>

**Open questions resolved by me (per user delegation):**

- Repo namespace = `krish2248/medxai`.
- License = MIT.
- Make wrapper = both `Makefile` and `make.ps1`.
- Phase-0 frontend = config files only; no Node toolchain.
- W&B / Dagshub / DVC / HF Hub setup = deferred per ADRs 0003–0004.

**Notes for next session.**

- Phase 0 is **complete** and the spec gating (Section 0 step 4) requires waiting for an explicit "go" before starting Phase 1.
- Phase 1 (data layer) will need a Kaggle API token and a Google Drive account before it can fully run; those credentials are not on this machine yet.
- First Phase-1 commit will be `chore(data): dvc init + .dvc/config` once the user confirms remote details.

---
