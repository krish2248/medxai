# MedXAI — Makefile (POSIX / WSL / macOS / Linux).
# Windows users: see make.ps1 — same targets, PowerShell flavour.
# All targets shell out to `uv run …` so behaviour matches CI exactly.

UV ?= uv
PYTHON ?= $(UV) run python

.DEFAULT_GOAL := help

.PHONY: help setup lock sync precommit-install lint format type test cov \
        train eval app api docs paper clean

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## One-time setup: sync deps + install pre-commit hooks.
	$(UV) sync --all-extras
	$(UV) run pre-commit install

lock: ## Refresh uv.lock without installing.
	$(UV) lock

sync: ## Install / update the env from uv.lock.
	$(UV) sync --all-extras

precommit-install: ## Install pre-commit hooks.
	$(UV) run pre-commit install

lint: ## Ruff lint + format check.
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format: ## Apply ruff fixes + formatting.
	$(UV) run ruff check . --fix
	$(UV) run ruff format .

type: ## Mypy strict on src/.
	$(UV) run mypy src/medxai

test: ## Run pytest suite (parallel, coverage on).
	$(UV) run pytest -n auto

cov: ## Run pytest with HTML coverage report.
	$(UV) run pytest -n auto --cov-report=html

# --- Phase-gated targets ---------------------------------------------------
# These print a friendly message until their phase lands. The targets
# themselves stay in the Makefile so the spec's command surface is stable.

train: ## (Phase 2+) Run a training experiment.
	@echo "[Phase 2+] training pipeline not yet implemented — see docs/PLAN.md"

eval: ## (Phase 2+) Evaluate a trained model.
	@echo "[Phase 2+] evaluation pipeline not yet implemented — see docs/PLAN.md"

app: ## (Phase 2+) Launch the Streamlit demo.
	@echo "[Phase 2+] Streamlit app not yet implemented — see docs/PLAN.md"

api: ## (Phase 7) Launch the FastAPI backend.
	@echo "[Phase 7] FastAPI backend not yet implemented — see docs/PLAN.md"

docs: ## (Phase 0+) Build MkDocs site locally.
	$(UV) run mkdocs build --strict

docs-serve: ## (Phase 0+) Serve MkDocs site at http://127.0.0.1:8000.
	$(UV) run mkdocs serve

paper: ## (Phase 8) Build the IEEE paper PDF.
	@echo "[Phase 8] paper build (LaTeX) not yet implemented — see docs/PLAN.md"

clean: ## Remove caches and build artefacts.
	@rm -rf .ruff_cache .mypy_cache .pytest_cache .coverage htmlcov coverage.xml site dist build
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
