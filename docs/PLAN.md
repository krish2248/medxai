# MedXAI — PLAN.md

This document is required by Section 0 of `MEDXAI_PROMPT (1).md`. It is the
first artifact created in the project. No other files will be created until
the user replies "go".

---

## 1. Restatement of the project (one paragraph)

MedXAI is a single, integrated medical-AI portfolio system that does three
things rigorously: (1) **predicts** on multi-modal medical inputs — five
imaging tasks (pneumonia CXR, ChestX-ray14, mammography patches, skin
lesions, diabetic retinopathy), eight tabular tasks (breast cancer FNA,
diabetes, heart, liver, kidney, stroke, Parkinson's, thyroid), and three
rule-based lab-report interpreters (CBC, urinalysis, lipid panel) trained on
public, license-permitting datasets; (2) **explains** every prediction with at
least two complementary XAI methods (Grad-CAM/Grad-CAM++/IG/Occlusion for
vision; SHAP/LIME/DiCE counterfactuals for tabular) plus quantitative
faithfulness scores (insertion/deletion AUC, sensitivity-n) and Adebayo
sanity checks; (3) **educates** through a Wellness Atlas of ten
human-curated, citation-backed preventive-health articles that ship as
versioned content in the repo, not generated content. The deliverable is
both a deployed product (FastAPI on HF Spaces, Streamlit demo, Next.js
landing on Vercel) and a research artifact (model cards, datasheets,
6–8-page IEEE-style paper with bootstrapped CIs, ablations, fairness
analysis, and a reproducibility statement). The project's contribution is
**integration + faithful explainability + curated wellness knowledge +
reproducibility**, not SOTA on any single benchmark.

---

## 2. Assumptions

These are the assumptions I am operating under. Any of them being wrong
changes the plan.

### Hardware
- Local development machine: Windows 11, PowerShell, no local CUDA GPU
  assumed. (Confirmed from environment.)
- Heavy training: free-tier Google Colab (T4) and/or Kaggle (P100/T4 x2),
  ~one solid GPU session per week. Spec Section 19 budgets HF Space CPU for
  inference, so trained weights must be small enough to serve on CPU.
- All Phase 0 work is CPU-only and runs on the local Windows machine.

### Tooling on Windows
- Python 3.11 will be installed (or installable) locally.
- `uv` is the package manager (Section 6); `poetry` is the documented
  fallback. I will assume `uv` is available or installable via `pip install
  uv` / `winget install astral-sh.uv`.
- `make` is not standard on Windows. Two options: (a) require `make` via
  Chocolatey/Scoop/WSL, (b) provide a parallel `make.ps1` PowerShell script
  with the same targets. I will propose **(b)** in Phase 0 as a documented
  ADR rather than mandate WSL — but flagged below as an open question.
- Docker Desktop is assumed installable but not required for Phase 0
  beyond having the Dockerfile/compose files present.

### Accounts / network
- A GitHub account exists; the repo will be created there once the user
  confirms the org/user namespace.
- HuggingFace and Vercel accounts will be created when Phase 8 (deploy)
  arrives — not blocking before then.
- Google Drive will be the DVC remote (Section 18). Authentication will be
  set up in Phase 1.
- Kaggle API token (`kaggle.json`) will be needed for several datasets in
  Phase 1.
- Network access to PyPI, GitHub, HuggingFace Hub, and Kaggle is
  available.

### Time / cadence
- Total runway: ~3–4 months elapsed, evenings + weekends.
- Sessions are intermittent; a `SESSION_LOG.md` will be appended to at the
  end of every working session (per user instruction).
- Phase boundaries are hard gates — I will not start Phase N+1 until the
  user explicitly types "go".

### Data
- All datasets listed in Sections 3.1 and 3.2 are still publicly available
  under their stated licenses. If any has been pulled (e.g., NIH ChestX-ray14
  occasionally has hosting changes), I will surface this in Phase 1 and
  propose a substitution by editing `MEDXAI_PROMPT.md` in the same PR.

---

## 3. Open questions (could change architecture)

I will not invent answers to these. They are flagged so the user can
resolve them before they cascade.

1. **Make on Windows.** Should Phase 0 ship `make.ps1` alongside `Makefile`,
   require WSL, or just document that contributors run the underlying
   commands directly? My default proposal: ship both `Makefile` and
   `make.ps1` (a thin wrapper invoking the same `uv run …` commands), and
   record the choice as an ADR. **This affects every "Done when: `make X`"
   acceptance criterion in the spec.**
2. **Git remote / namespace.** What GitHub user or org should the repo be
   pushed to? Until I know, I will keep the repo local and skip the
   `git remote add` step. CI workflows will be committed but not run until
   the repo is on GitHub.
3. **CI gating before there is a remote.** Section 14 mandates GitHub
   Actions on every PR, and Section 0 says Phase 0 is done "when CI is
   green on a fresh clone." If we are local-only at end of Phase 0, the
   "CI green" check shifts to "the workflow files are syntactically valid
   and `act` (or a manual run after pushing) reports green on first run."
   Confirm this interpretation.
4. **HF Hub / DVC remote setup timing.** Setting up the Google Drive DVC
   remote and HF Hub repos can be deferred to Phase 1 and Phase 8
   respectively. Confirming this avoids blocking Phase 0 on credentials.
5. **Optional W&B / Dagshub.** Spec says these are optional. Default: skip
   in Phase 0; revisit before Phase 2 (training).
6. **Next.js scaffold in Phase 0?** Section 5 + 11 + 13 specify the
   `frontend/` directory and Tailwind theme tokens, but Phase 0 only
   explicitly mentions locking the Tailwind config. I will scaffold an
   empty `frontend/` with `tailwind.config.ts` + `globals.css` + the theme
   linter, but **not** run `pnpm create next-app` until Phase 7 — confirm
   this read.
7. **License of the project.** Spec says MIT (Section 13). Confirming so
   Phase 0 commits the right `LICENSE` file.

---

## 4. Confirmation of phase order (Section 20)

I confirm the phase order from Section 20 verbatim and will execute in this
sequence:

| Phase | Scope (one line) |
|---|---|
| 0 | Scaffolding: repo, tooling, theme tokens, CI skeleton, MkDocs skeleton, docker-compose |
| 1 | Data layer: DVC, downloaders, synthetic generators, datamodules, splits, datasheets |
| 2 | Tabular MVP on WDBC (proves the full predict→explain→guidance→PDF loop end to end) |
| 3 | Vision MVP: DenseNet121 on Kermany pneumonia + Grad-CAM/IG + faithfulness + sanity checks |
| 4 | Vision scale-up: ChestX-ray14, mammography, derm, DR; backbone comparison; ViT ablation |
| 5 | Remaining tabular (7 tasks) + lab-report rule engines (CBC/urinalysis/lipid) |
| 6 | Wellness Atlas: 10 articles, citation linter, rendering in Streamlit + Next.js |
| 7 | API feature-complete + Next.js landing on Vercel calling the API |
| 8 | Deploy (HF Spaces, Vercel, GH Pages), MkDocs site, paper, slides, v1.0.0 tag |
| 9 | Polish: demo GIF, hostile-reviewer pass, ethics & limitations final pass |

Stretch goals (Section 23) are deferred and will only be considered after
Phase 8 is green.

---

## 5. First 10 git commits I intend to make in Phase 0 (in order)

These are conventional-commits style. Each commit has tests where the spec
requires them (Section 22 rule: "Every function in src/ has a test before
the function is committed"). Phase 0 has very little executable code in
`src/`, so most early commits are pure scaffolding; tests appear from
commit 7 onward when the first real Python utility lands.

1. **`chore(repo): initial empty repo with .gitignore, .gitattributes, LICENSE (MIT), CITATION.cff`**
   – Sets the legal and VCS baseline. Ensures `data/`, model artifacts,
   `__pycache__/`, `.venv/`, `node_modules/`, `.dvc/cache` are ignored from
   commit zero.
2. **`docs(readme): add README skeleton with disclaimer, quickstart placeholders, and 30-second pitch`**
   – Disclaimer (Section 11.4) appears verbatim. README is intentionally
   short per Section 16.
3. **`build(deps): add pyproject.toml with pinned tool versions and ruff/mypy config; commit uv.lock`**
   – Python 3.11, all libs from Section 6 listed under `[project]` + extras
   for `dev`, `vision`, `tabular`, `xai`, `app`, `docs`. ruff (lint+format)
   and mypy (`--strict` on `src/`) configured here.
4. **`chore(scaffold): add pre-commit config (ruff, mypy, eof-fixer, trailing-ws, check-yaml/toml, detect-secrets, nbstripout)`**
   – Per Section 14. Hooks installable with `pre-commit install`.
5. **`feat(pkg): create src/medxai package with __init__.py exposing __version__`**
   – Empty package + version stamp. This is the smallest src/ artifact that
   the test in commit 7 can import.
6. **`build(make): add Makefile and make.ps1 with setup/lint/test/train/eval/app/docs/paper targets`**
   – Cross-platform targets so `make X` and `./make.ps1 X` do the same
   thing. ADR `0001-cross-platform-make.md` recorded under
   `docs/decisions/`. (Pending answer to open question 1; if the user
   prefers a different approach this commit will change.)
7. **`test(pkg): add tests/unit/test_version.py and pytest config; assert importable __version__ matches pyproject`**
   – First real test. Establishes the testing pattern (pytest, coverage,
   `tests/{unit,integration,property,e2e,visual}` layout) before any
   non-trivial src/ code lands.
8. **`feat(theme): lock white theme tokens — streamlit_app/.streamlit/config.toml and frontend/tailwind.config.ts + globals.css`**
   – Section 11.1 colors/tokens, Section 11.2 streamlit theme, Section 11.3
   tailwind theme. No Next.js scaffold yet — only the config files needed
   for the theme linter to have something to read.
9. **`feat(ci): add scripts/lint_theme.py + tests; fails on bg-black / bg-zinc-900 / dark-mode-only patterns under frontend/ and streamlit_app/`**
   – Section 14 step 7 (theme linter). Tests cover positive (clean file
   passes) and negative (file with `bg-black` fails) cases.
10. **`ci(actions): add .github/workflows/ci.yml — uv setup, sync, ruff, mypy, pytest with 80% coverage gate, theme linter, docker build`**
    – The Phase 0 acceptance gate. Wellness-atlas linter (Section 14 step
    6) is stubbed to a no-op for now (no articles exist until Phase 6) but
    wired in.

After commit 10, the remaining Phase 0 work is small: MkDocs skeleton,
docker-compose, docker/api.Dockerfile, docker/streamlit.Dockerfile,
CHANGELOG.md scaffold, CONTRIBUTING.md, SECURITY.md, .env.example. Those
will land in commits 11–14 (still Phase 0). The final wrap-up commit
**`chore(scaffold): initialize project structure`** from Section 0 will be
either a merge commit or a documentation-only commit summarizing the
phase, depending on what the user prefers when we get there.

---

## 6. What I am doing now

Per Section 0 / step 2: **STOP**. I will not create any other file.
Waiting for the user to reply "go" before starting Phase 0.

When "go" arrives, I will execute commits 1–10 above (and any remaining
Phase 0 work), get CI green, summarize the diff, and stop again.
