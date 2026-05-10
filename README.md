<!-- markdownlint-disable MD041 -->
<div align="center">

# MedXAI

**Multi-Modal Medical Explainable AI + Wellness Atlas**

*Predict, explain, and learn from medical data — responsibly.*

[![CI](https://github.com/krish2248/medxai/actions/workflows/ci.yml/badge.svg)](https://github.com/krish2248/medxai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

---

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions. If you have a medical concern, consult a licensed clinician.**

---

## What this is

MedXAI is one product that does three things and does them rigorously:

1. **Predict** — multi-modal medical AI: classifies medical images and interprets structured medical reports / clinical features.
2. **Explain** — every prediction ships with at least two complementary XAI methods plus a quantitative faithfulness score. Saliency is treated as a hypothesis, not proof.
3. **Educate** — a curated **Wellness Atlas** of preventive-health knowledge (plastics, cookware, water, food, alcohol, air, sleep, micronutrients, screening calendars, red-flag symptoms). Every article is human-curated from cited primary sources.

This is a **portfolio + research artifact**, deployed to HF Spaces (Streamlit + FastAPI) and Vercel (Next.js landing). It is also an MSc-application piece: model cards, datasheets, a 6–8-page IEEE-style paper, ablations, fairness analysis, and a reproducibility statement live in this repo alongside the code.

The full specification is in [`MEDXAI_PROMPT.md`](MEDXAI_PROMPT.md) — that document is the single source of truth for the project. The phased plan is in [`docs/PLAN.md`](docs/PLAN.md).

---

## What this is NOT

- Not a CE/FDA-cleared diagnostic device.
- Not a substitute for a clinician.
- Not trained on private patient data — only public, license-permitting, de-identified datasets.
- Not aiming for SOTA on any single benchmark — the contribution is **integration + explainability + curated wellness knowledge + reproducibility**.
- Not auto-generating awareness content with an LLM. Every Wellness Atlas article is human-reviewed against cited primary sources.

---

## Quickstart

> Phase 0 scaffolding only. The commands below will fill out as later phases land.

```bash
# 1. Install uv (https://docs.astral.sh/uv/) and Python 3.11
# 2. Sync the project
uv sync --all-extras

# 3. Install pre-commit hooks
uv run pre-commit install

# 4. Lint / type-check / test
make lint    # or:  ./make.ps1 lint        on Windows PowerShell
make test    # or:  ./make.ps1 test
```

Heavier commands (`make train`, `make app`, `make docs`, `make paper`) become available as their phases land — see `docs/PLAN.md`.

---

## Architecture (target)

```
Next.js (Vercel) ──┐
                   ├─► FastAPI (HF Spaces, Docker) ─► Image / Tabular / Lab / Guidance / Wellness
Streamlit (HF) ────┘
```

Streamlit is the demo surface. Next.js is the polished landing. Both call the **same** FastAPI backend — no model duplication.

---

## Project status

| Phase | Status |
|---|---|
| 0 — Scaffolding | ✅ complete (2026-05-10) |
| 1 — Data layer | not started |
| 2 — Tabular MVP (WDBC end-to-end) | not started |
| 3 — Vision MVP (Kermany pneumonia) | not started |
| 4 — Vision scale-up (CXR14 / mammo / derm / DR) | not started |
| 5 — Remaining tabular + lab interpreters | not started |
| 6 — Wellness Atlas (10 articles) | not started |
| 7 — API + Next.js | not started |
| 8 — Deploy + docs + paper | not started |
| 9 — Polish | not started |

A daily progress log lives in [`SESSION_LOG.md`](SESSION_LOG.md).

---

## Documentation

- [`MEDXAI_PROMPT.md`](MEDXAI_PROMPT.md) — full project specification (single source of truth).
- [`docs/PLAN.md`](docs/PLAN.md) — restatement, assumptions, open questions, commit plan.
- `docs/decisions/` — Architecture Decision Records (ADRs).
- `docs/` (later: MkDocs Material site) — datasheets, model cards, XAI methodology, evaluation, reproducibility, ethics & limitations.

---

## License

[MIT](LICENSE). See `MEDXAI_PROMPT.md` Sections 11.4 and 16 for usage limits and the disclaimer that must accompany predictions.

---

## Citation

If you use MedXAI in academic work, see [`CITATION.cff`](CITATION.cff). A formal `bibtex` block will be added once the v1.0.0 paper is tagged.
