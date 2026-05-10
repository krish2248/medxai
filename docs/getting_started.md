# Getting started

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions. If you have a medical concern, consult a licensed clinician.**

This is the **Phase 0** quickstart — only the scaffolding is real. Each later
phase adds its own commands here as it lands.

## 1. Prerequisites

| Tool | Version | Why |
|---|---|---|
| Python | 3.11.x | Pinned in `.python-version` and `pyproject.toml` |
| [uv](https://docs.astral.sh/uv/) | ≥ 0.5 | Package manager and venv driver |
| git | 2.40+ | Source control |
| GNU make *or* PowerShell 5+ | — | Either `make` (POSIX) or `./make.ps1` (Windows) |

Install uv:

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Clone and set up

```bash
git clone https://github.com/krish2248/medxai.git
cd medxai
make setup            # POSIX
./make.ps1 setup      # PowerShell
```

`make setup` runs `uv sync --all-extras` and installs the pre-commit hooks.

## 3. Verify

```bash
make lint    # ruff check + ruff format --check
make type    # mypy strict on src/medxai
make test    # pytest with coverage gate
```

All three should pass on a fresh clone. CI runs the same commands plus the
theme and wellness linters.

## 4. What's next

The training, app, and API targets (`make train`, `make app`, `make api`,
`make paper`) print a "not yet implemented" message in Phase 0. They become
real as later phases land — see [`PLAN.md`](PLAN.md).
