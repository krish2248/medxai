# Contributing to MedXAI

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions.**

Thanks for considering a contribution. MedXAI is currently a single-author
portfolio project (see `MEDXAI_PROMPT.md`), so external PRs are welcome but
the spec in that file is authoritative — material changes need agreement
before code lands.

## Ground rules from the spec

- No fabricated metrics, no placeholder weights, no `# TODO` merged to `main`.
- Every function in `src/medxai/` has a test **before** the function is committed.
- Every dataset has a datasheet; every model has a model card; every Wellness Atlas article has at least two citations from the approved source list (Section 4.3 of `MEDXAI_PROMPT.md`).
- The disclaimer in Section 11.4 appears verbatim wherever predictions or guidance is shown.
- The visual theme is locked white (Section 11.1). The CI theme linter rejects `bg-black`, `bg-zinc-900`, `dark:` utilities, and Tailwind `darkMode` config.
- If reality contradicts the spec (a library is gone, a dataset moved, a model is too large for free-tier GPU), update `MEDXAI_PROMPT.md` in the same PR.
- Architecture-changing question → open an issue first. Pure style call → decide and log it as an ADR in `docs/decisions/`.

## Local setup

```bash
# 1. Install Python 3.11 and uv (https://docs.astral.sh/uv/).
# 2. Clone and bootstrap.
git clone https://github.com/krish2248/medxai.git
cd medxai
make setup            # POSIX
./make.ps1 setup      # PowerShell on Windows
```

`make setup` is a thin wrapper around `uv sync --all-extras` plus
`uv run pre-commit install`.

## Local checks (mirror CI)

```bash
make lint    # ruff check + ruff format --check
make type    # mypy strict on src/medxai
make test    # pytest with coverage
uv run python -m scripts.lint_theme
uv run python -m scripts.lint_wellness
```

CI runs all of the above on every push and pull request to `main`.

## Branching & commits

- Work on a feature branch (`feat/<short-slug>`, `fix/<short-slug>`, `docs/<short-slug>`).
- Use Conventional Commits — the existing history shows the style.
- Open a PR against `main`; CI must be green; squash-merge unless the diff is tiny.
- Never `git push --force` to `main`.

## Code style

- Python 3.11+ syntax. `from __future__ import annotations` at the top of every module.
- Type-annotate every public function. `mypy --strict` is the gate.
- Docstrings: Google style. Be terse; comments explain *why*, not *what*.
- Tests live next to the layer they cover (`tests/unit/`, `tests/integration/`, etc.).

## Reporting security issues

See [`SECURITY.md`](SECURITY.md). Do not file public issues for security reports.
