# MedXAI — Multi-Modal Medical Explainable AI + Wellness Atlas

> Single-source-of-truth specification for the project.
> Scope: **one B.Tech student, ~3–4 months, free-tier compute (Colab / Kaggle), one solid GPU session a week at most**.
> Goal: a portfolio piece strong enough to anchor a German MSc application in AI/ML.

---

## 0. OPENING MESSAGE — paste this as your first message to Claude Code

Copy everything inside the fence and send it as your first user message in a fresh Claude Code session. Then attach this file (`MEDXAI_PROMPT.md`) at the repo root.

```
You are the lead engineer on MedXAI. The full specification is in MEDXAI_PROMPT.md.
Read it end-to-end before writing a single file.

Then do exactly this, in order:

1) Write docs/PLAN.md containing:
   - One-paragraph restatement of the project in your own words.
   - Assumptions you are making (hardware, accounts, network, time).
   - Open questions that would change the architecture.
   - Confirmation of the phase order in Section 20.
   - The first 10 git commits you intend to make in Phase 0, in order.

2) STOP. Do not create any other file. Wait for me to say "go".

3) When I say "go", execute Phase 0 only. After Phase 0:
   - All CI checks green on a fresh clone.
   - Commit: chore(scaffold): initialize project structure
   - Show the diff summary and the CI run URL.
   - Stop and wait for "go" again.

4) Repeat (3) for every subsequent phase.

Hard rules:
- No fabricated metrics, no placeholder weights, no "# TODO" merged to main.
- Every function in src/ has a test before the function is committed.
- Every dataset has a datasheet; every model has a model card; every Wellness Atlas
  article has at least two citations from the approved source list (Section 4.3).
- The disclaimer in Section 11.4 appears verbatim wherever required.
- The visual theme is locked white (Section 11.1). Do not introduce dark mode.
- If reality contradicts the spec (a library is gone, a dataset moved, a model is
  too large for free-tier GPU), update MEDXAI_PROMPT.md in the same PR. The spec
  evolves with the code.
- If you are uncertain about anything that affects architecture, stop and ask.
  If it is purely a style call, decide and log it as an ADR in docs/decisions/.

Begin with step (1).
```

---

## 1. Vision

MedXAI is one product that does three things and does them rigorously:

1. **Predict** — multi-modal medical AI: classifies medical images and interprets structured medical reports / clinical features.
2. **Explain** — every prediction is shipped with at least two complementary XAI methods plus a quantitative faithfulness score. Saliency is treated as a hypothesis, not proof.
3. **Educate** — a curated **Wellness Atlas** of preventive-health knowledge (plastics, cookware, water, food, alcohol, air, sleep, micronutrients, screening calendars). Every article is human-curated from cited primary sources.

The deliverable is simultaneously a **product** (deployed to HF Spaces + Vercel) and a **research artifact** (technical report, model cards, datasheets, reproducibility statement, ablations, fairness analysis).

---

## 2. Non-goals — state these in the README

- Not a CE/FDA-cleared diagnostic device.
- Not a substitute for a clinician.
- Not trained on private patient data — only public, license-permitting, de-identified datasets.
- Not aiming for SOTA on any single benchmark — the contribution is **integration + explainability + curated wellness knowledge + reproducibility**.
- Not auto-generating awareness content with an LLM. Every Wellness Atlas article is human-reviewed against cited primary sources.

This is a portfolio project. Honesty about scope is itself a feature.

---

## 3. Realistic scope — what we will actually train

### 3.1 Imaging models we train end-to-end (5)

| Model | Task | Dataset | Why this dataset |
|---|---|---|---|
| `pneumo-net` | Binary pneumonia (chest X-ray) | Kermany Pediatric CXR | Tiny, clean, trains in <1 h on free Colab |
| `cxr14-net` | 14-class multi-label CXR | NIH ChestX-ray14 | Canonical research benchmark |
| `mammo-net` | Malignant vs benign | CBIS-DDSM patches | Public, patch-level keeps it tractable |
| `derm-net` | 7-class skin lesion | HAM10000 | Small (~10k), permissive license |
| `dr-net` | Diabetic retinopathy 5-grade | APTOS 2019 | Kaggle, ~3.6k, manageable |

Backbones: **DenseNet121** (CXR canon), **EfficientNet-B0** (small/fast), **ResNet50** (general). Train DenseNet + EfficientNet on every task; one ViT-B/16 ablation on `cxr14-net` for the paper.

### 3.2 Tabular models (8)

| Model | Task | Dataset |
|---|---|---|
| `bc-tab` | Breast cancer FNA | UCI Wisconsin Diagnostic |
| `dm-tab` | Diabetes risk | Pima Indians + BRFSS Diabetes Health Indicators (subset) |
| `heart-tab` | Heart disease | UCI Cleveland + Statlog Heart |
| `liver-tab` | Liver disease | Indian Liver Patient |
| `ckd-tab` | Chronic kidney disease | UCI CKD |
| `stroke-tab` | Stroke risk | Kaggle Healthcare Stroke |
| `parkinsons-tab` | Parkinson's voice | UCI Parkinson's |
| `thyroid-tab` | Thyroid function | UCI Thyroid (sick/hypo/hyper) |

Three baselines per task: **LogReg, RandomForest, XGBoost** (+ LightGBM if a deadline allows). Optuna 50-trial sweep, 5-fold stratified CV, isotonic calibration.

### 3.3 Lab-report interpreters — rules + light ML (3)

Real labeled lab datasets are scarce. We use a **rules-first, ML-second** approach with **synthetic but reference-range-grounded** data. Every reference range is cited from Mayo / MedlinePlus / Tietz / NHS / AAFP in `configs/reference_ranges/*.yaml`.

- `cbc-interpreter` — Complete Blood Count: Hb, HCT, RBC, WBC + differential, platelets, MCV/MCH/MCHC, RDW. Patterns labeled: iron-deficiency anemia, B12/folate deficiency, infection, thrombocytopenia, leukocytosis, etc.
- `urinalysis-interpreter` — pH, SG, protein, glucose, ketones, blood, leukocytes, nitrites. Patterns: UTI, dehydration, glycosuria, proteinuria.
- `lipid-interpreter` — TC, LDL, HDL, TG, non-HDL, ratios → ATP-IV-style risk band.

The synthetic generator and labeling rules are deterministic, seeded, and version-controlled. The dataset card states clearly: *"synthetic, rule-grounded; for educational and XAI demonstration; not validated against real patient cohorts."*

### 3.4 Tier 2 — wrapped, not trained (stretch / breadth)

Where we want breadth without training time, we wrap a HuggingFace model behind the same prediction + XAI interface and label it clearly as `pretrained:hf`:

- `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` — biomedical image–text similarity for retrieval-style demos.
- `microsoft/rad-dino` — radiology-pretrained DINOv2 features (frozen embedder, not finetuned).

Tier 2 is **clearly tagged in the UI** so a reviewer never confuses pretrained-and-wrapped with trained-from-scratch.

---

## 4. Wellness Atlas — curated educational content

This is what makes the project feel like a real product, not just a Kaggle clone. It is **not AI-generated**. It is a structured, citation-backed knowledge base that I write and Claude formats.

### 4.1 Article topics (10 evergreen articles for v1)

1. **Plastics & your body** — BPA, BPS, phthalates, microplastics; what to swap; what the evidence actually says.
2. **Cookware safety** — non-stick (PFAS/PTFE/PFOA), aluminum, cast iron, stainless, ceramic, copper. Realistic guidance.
3. **Water quality** — common contaminants (lead, chlorine byproducts, nitrates, PFAS), filter types (carbon, RO, UV), bottled vs tap.
4. **Food awareness** — ultra-processed foods, additives worth knowing, oxidized seed oils — separating signal from social-media noise.
5. **Alcohol & health** — current evidence (no safe lower bound for several outcomes per WHO 2023).
6. **Air quality** — PM2.5, indoor VOCs, radon, ventilation basics, when to mask.
7. **Sleep** — minimum sleep, circadian disruption, shift-work risk.
8. **Micronutrients** — when to test (Vit D, B12, ferritin, magnesium), when supplementation actually helps.
9. **Screening calendars** — adult preventive-care schedule by age and sex (USPSTF / NHS).
10. **Red flags — when to see a doctor** — symptoms that need same-day care; symptoms that need same-week care.

### 4.2 Article schema (every article must conform)

```yaml
slug: plastics-and-your-body
title: Plastics and your body
last_reviewed: 2025-MM-DD
reading_minutes: 7
tldr: |
  Two paragraphs maximum.
key_points:
  - Bullet 1
  - Bullet 2
sections:
  - heading: What the evidence says
    body: |
      Markdown body...
  - heading: Practical swaps
    body: |
      ...
red_flags:
  - When to see a doctor
sources:                       # minimum 2, ideally 4+
  - title: WHO factsheet on microplastics in drinking water
    url: https://...
    org: WHO
    year: 2019
    tier: 1                    # 1 = primary org / systematic review; 2 = peer-reviewed; 3 = reputable secondary
disclaimer: standard           # uses Section 11.4 verbatim
related_articles:
  - cookware-safety
  - water-quality
```

### 4.3 Approved sources — tiered

- **Tier 1 (primary / authoritative):** WHO, EPA, EFSA, FDA, CDC, NHS, NICE, USPSTF, AAFP, Cochrane Reviews, NIEHS, ATSDR, EPA IRIS.
- **Tier 2 (peer-reviewed):** PubMed-indexed systematic reviews and meta-analyses; high-quality cohort studies.
- **Tier 3 (reputable secondary):** MedlinePlus, Mayo Clinic, Cleveland Clinic, EWG (used carefully and labeled).

**Every article cites at least one Tier 1 source.** No personal blogs, no influencer content, no Wikipedia as primary citation.

### 4.4 Strict rule

The Wellness Atlas pages are **rendered from YAML/MDX**, not generated at request time. The content lives in `content/wellness/*.md` (front-matter + markdown), is reviewed in PR like code, and ships in the repo. The CI has a step that fails the build if any article has fewer than two citations or is missing the disclaimer.

---

## 5. Homepage layout — what the user sees first

The homepage is the showpiece. It is dense with information, all in white theme, all real (no Lorem Ipsum, no fake metrics).

### 5.1 Sections, top to bottom

1. **Hero** — single sentence: *"Predict, explain, and learn from medical data — responsibly."* + standard disclaimer banner immediately below + two buttons: *Try a demo* / *Read the docs*.
2. **KPI strip — four cards in a row:**
   - Total models shipped (live number)
   - Total predictions served (read from the API stats endpoint)
   - Datasets integrated
   - Wellness articles published
3. **"What MedXAI does" — three blocks** with icons: Predict / Explain / Educate.
4. **Population analytics dashboard — the visual heart of the page.** All Plotly, all interactive, all clearly labeled *"illustrative — sourced from public aggregates"*:
   - **Donut chart:** modality distribution (CXR / mammography / derm / DR / tabular).
   - **Stacked bar:** disease prevalence by modality.
   - **Heatmap:** age band × condition (rows: 0–18, 19–35, 36–50, 51–65, 66+; cols: top 10 conditions).
   - **Line chart:** condition severity / fatality trend over time (sourced from public WHO/IHME aggregates, labeled).
   - **Choropleth (world map):** burden by region for one chosen condition (e.g., TB or DR), with a dropdown.
   - **Radar chart:** model performance across metrics (AUROC, F1, AUPRC, precision, recall, calibration).
   - **Treemap:** disease burden grouped by category (cardiovascular / respiratory / metabolic / oncology / neurological).
   - **Sankey diagram:** patient journey (symptom → modality → finding → next step), illustrative.
5. **Model gallery — grid of cards.** Each card: model name, modality, headline AUROC with bootstrapped 95% CI, dataset, *Try* button, *Model card* link.
6. **Wellness Atlas strip — horizontally scrolling cards** of the 10 articles, each with title, reading time, last-reviewed date.
7. **"Things to look out for" — red-flag block** rendered from the *Red flags* article: a clean grid of symptoms grouped by *same-day care* / *same-week care*, with a clear "this is not medical advice" banner above.
8. **Methodology strip — three blocks:** XAI methodology, evaluation methodology, reproducibility statement (each links to its docs page).
9. **Footer:** repo link, paper PDF, slides, license, citation block, contact.

### 5.2 Charts — implementation

- All interactive charts use **Plotly** (Python in Streamlit, JS in Next.js — same chart specs serialized as JSON).
- All static charts that go into the paper use **matplotlib + seaborn** with a project-wide stylesheet (`reports/figures/medxai.mplstyle`) so figures look consistent.
- A `src/medxai/viz/` module exposes one function per chart type. The Streamlit homepage and the FastAPI `/v1/stats/*` endpoints both call into this module — chart logic is never duplicated.

---

## 6. Tech stack (locked)

| Layer | Choice |
|---|---|
| Language | Python 3.11 |
| DL | PyTorch 2.x, torchvision, timm |
| Tabular | scikit-learn, XGBoost, LightGBM |
| XAI | Captum, SHAP, LIME, DiCE-ML |
| Data | pandas, numpy, polars (large CSVs) |
| Plotting | Plotly (interactive), matplotlib + seaborn (static / paper) |
| Image aug | Albumentations |
| Tracking | MLflow (local); optional W&B if I add a key |
| Data versioning | DVC + remote on Google Drive |
| Config | Hydra |
| API | FastAPI + Pydantic v2 |
| Demo UI | Streamlit (multi-page) |
| Polished UI | Next.js 14 (App Router) + Tailwind + shadcn/ui + Plotly.js |
| PDF reports | WeasyPrint |
| Containers | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Lint/format/types | ruff (lint+format), mypy --strict on src/ |
| Testing | pytest, pytest-cov, hypothesis, Playwright (E2E + visual) |
| Docs | MkDocs Material + mkdocstrings |
| Pre-commit | pre-commit framework |
| Package mgmt | uv (poetry as fallback) |

Pin everything in `pyproject.toml` and commit `uv.lock`.

---

## 7. Architecture

```
                    ┌───────────────────────────────────┐
                    │        Next.js (Vercel)            │
                    │  Landing + Dashboard + Try-It UI   │
                    └──────────────┬────────────────────┘
                                   │ HTTPS / JSON
                                   ▼
                    ┌───────────────────────────────────┐
                    │      FastAPI (HF Spaces, Docker)   │
                    │  /predict /explain /report /stats  │
                    │  /wellness  (serves Atlas content) │
                    └──────────────┬────────────────────┘
                                   │
       ┌─────────────┬─────────────┼─────────────┬─────────────┐
       ▼             ▼             ▼             ▼             ▼
  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Image   │  │ Tabular  │  │ Lab      │  │ Guidance │  │ Wellness │
  │ infer   │  │ infer    │  │ rules    │  │ rules    │  │ MD/YAML  │
  └─────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
       │             │
       ▼             ▼
   ┌────────┐    ┌────────┐
   │ XAI:   │    │ XAI:   │
   │ Captum │    │ SHAP/  │
   │        │    │ LIME   │
   └────────┘    └────────┘

  Parallel surface:
                    ┌───────────────────────────────────┐
                    │     Streamlit (HF Spaces)          │
                    │   Multi-page demo, same backend    │
                    └───────────────────────────────────┘
```

Streamlit ships first and is what reviewers click. Next.js is the polished surface. Both call the **same** FastAPI backend — no model duplication.

---

## 8. ML pipeline

```
configs/<task>.yaml ─► DataModule ─► Model ─► Trainer ─► Evaluator ─► MLflow run
                                                                          │
                                                                          ▼
                                                                    Model card MD
```

### 8.1 Image training

- ImageNet pretraining → freeze → finetune head → unfreeze later layers.
- Albumentations: random crop, flip, brightness/contrast, CLAHE, slight rotation. **No L/R flip on chest X-rays unless the L/R laterality marker is removed first.**
- Loss: BCEWithLogitsLoss for multi-label, focal for imbalance, weighted CE for binary imbalance.
- AdamW, cosine schedule with warmup, mixed precision.
- Input size: 224 baseline, 384 for one "best" run per task.

### 8.2 Tabular training

- Three baselines per task: LR, RandomForest, XGBoost.
- Optuna 50 trials, 5-fold stratified CV, MedianPruner.
- Probability calibration (isotonic). Calibration curves go in the paper.

### 8.3 Mandatory metrics (for every model)

- Per-class precision, recall, F1, AUROC, AUPRC, sensitivity, specificity.
- Macro and micro averages.
- Confusion matrix (raw + normalized).
- Brier score + reliability diagram (calibration).
- **Bootstrapped 95% CIs** on the headline metric (`n_boot=1000`, mean ± CI, never bare point estimates).
- McNemar's test when comparing top two models on the same test set.
- Fairness: per-subgroup metrics on age band and sex where the dataset has them; equalized-odds gap.
- Robustness: Δ-accuracy under Gaussian noise + brightness shift.

### 8.4 Reproducibility — every model card includes

Random seed (Python / NumPy / PyTorch / CUDA) · library versions · hardware · wall-clock training time · exact data split (CSV of indices, hashed) · config hash · MLflow run ID.

---

## 9. XAI

### 9.1 Vision

A single `Explainer` protocol with concrete classes: `GradCAMExplainer`, `GradCAMPlusPlusExplainer`, `IntegratedGradientsExplainer`, `OcclusionExplainer`.

- **Sanity checks** (Adebayo et al. 2018): randomize weights, randomize labels, verify saliency degrades. A saliency map that survives weight randomization is not faithful — and we say so in the docs.
- **Quantitative XAI metrics:** insertion AUC, deletion AUC, sensitivity-n. Implemented in `src/medxai/xai/faithfulness.py`.
- **Side-by-side viewer:** original | Grad-CAM | IG | agreement heatmap (cosine similarity of normalized maps).

### 9.2 Tabular

- TreeSHAP (XGBoost / LightGBM / RF — exact, fast).
- KernelSHAP (model-agnostic comparison).
- LIME (run `n=10` times to expose its instability — show variance bands).
- DiCE counterfactuals: smallest feature change that flips the prediction.
- Both global (mean |SHAP|, summary plot) and local (waterfall, force plot) views.

### 9.3 Honesty page in the docs

Saliency ≠ causation. Grad-CAM is class-discriminative but coarse. LIME is unstable. A confident model + a clean Grad-CAM is **not** evidence the model is right — it might be exploiting a shortcut (laterality marker, hospital text, scanner artifact).

---

## 10. Suggestion engine

A pure-Python rules module: `src/medxai/guidance/`. Takes `(prediction, confidence, optional patient_context)` and returns structured guidance:

```python
class Guidance(BaseModel):
    severity: Literal["info", "low", "moderate", "high", "urgent"]
    next_steps: list[str]
    red_flags: list[str]      # see-a-doctor-now items
    citations: list[Citation]
    disclaimer: str           # always Section 11.4 verbatim
```

Rules are in YAML (`src/medxai/guidance/rules/*.yaml`) with **citations to public guidelines** (WHO, NICE, USPSTF, AAFP, MedlinePlus). No rule ships without a citation. The CI fails if any rule is missing one.

---

## 11. UI / UX — locked rules

### 11.1 Visual theme — WHITE, locked

| Token | Value |
|---|---|
| Background | `#FFFFFF` |
| Surface | `#FAFAFA` |
| Border | `#E5E7EB` |
| Text primary | `#111827` |
| Text secondary | `#4B5563` |
| Text muted | `#9CA3AF` |
| Accent (single) | `#2563EB` (clinical blue) |
| Success | `#059669` (emerald) |
| Warning | `#D97706` (amber) |
| Danger | `#DC2626` (red) — used only for red-flag content |
| Shadow | `0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04)` |

Typography: **Inter** for UI, **JetBrains Mono** for code, **Source Serif 4** for long-form Wellness Atlas reading.

Rules:

- No dark mode in v1. If a user requests it later, add it via `prefers-color-scheme`, but the default and screenshots stay white.
- Accent color is **used sparingly** — primary buttons, active nav, key-data highlights. Never on backgrounds.
- All Plotly charts use a custom `medxai_white` template (white paper, white plot bg, light gray gridlines, accent-blue series).
- All matplotlib figures use the same palette via `reports/figures/medxai.mplstyle`.
- Generous whitespace. Card padding ≥ 24 px. Section spacing ≥ 64 px on desktop.
- Soft shadows only. Never harsh borders alone.
- Icons: **Lucide** (consistent stroke, neutral, free).

### 11.2 Streamlit theme

`.streamlit/config.toml`:
```toml
[theme]
base = "light"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FAFAFA"
textColor = "#111827"
primaryColor = "#2563EB"
font = "sans serif"
```

### 11.3 Next.js theme

Tailwind config locks the same tokens. `globals.css` defines CSS variables. shadcn/ui components use the locked tokens. No `bg-zinc-900`, no `bg-black`, no dark-mode-only patterns anywhere in the codebase. CI fails the build if any of those strings appear in `frontend/`.

### 11.4 Disclaimer (verbatim, used everywhere)

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions. If you have a medical concern, consult a licensed clinician.**

This appears: above every prediction result, in every PDF report header, on the landing page hero, in the README, at the top of the FastAPI OpenAPI description, at the top of every Wellness Atlas article.

### 11.5 Pages — Streamlit

- **Home** — Section 5 layout.
- **Chest X-ray** — upload → predict → top-k probs → Grad-CAM | IG side by side → guidance → PDF report.
- **Mammography** — same flow on patches.
- **Skin lesion** — same flow on HAM10000-style input.
- **Diabetic retinopathy** — same flow on fundus images.
- **Breast cancer (tabular)** — 30-feature form → predict → SHAP waterfall → DiCE counterfactual → guidance.
- **Diabetes / Heart / Liver / Kidney / Stroke / Parkinson's / Thyroid (tabular)** — one combined page with task selector to keep the sidebar clean.
- **Lab reports** — paste/CSV upload of CBC / urinalysis / lipid → rule-based interpretation with patterns highlighted.
- **XAI Comparison** — pick a sample, pick two methods, see them rendered side by side + insertion/deletion curves.
- **Wellness Atlas** — list of articles, search bar, tags. Clicking opens the rendered article.
- **About / Disclaimer / Citations**.

### 11.6 Pages — Next.js

- `/` — landing (Section 5).
- `/dashboard` — analytics, polished.
- `/try/[modality]` — drag-and-drop demo per modality.
- `/wellness` — Wellness Atlas index.
- `/wellness/[slug]` — article reader.
- `/docs` — MDX subset of MkDocs.

### 11.7 Accessibility

WCAG AA. Keyboard navigation. Alt text on every image. `prefers-reduced-motion` respected. Color contrast checked in CI via `pa11y` on every Next.js page.

---

## 12. Backend API

```
POST /v1/predict/image          { modality, image (base64 or multipart) }
POST /v1/predict/tabular        { task, features }
POST /v1/predict/lab            { kind: cbc|urinalysis|lipid, values }
POST /v1/explain/image          { modality, image, method }
POST /v1/explain/tabular        { task, features, method }
POST /v1/report                 { prediction_id }            # PDF
GET  /v1/stats/overview                                       # KPI cards
GET  /v1/stats/age_disease                                    # heatmap
GET  /v1/stats/model_perf                                     # gallery
GET  /v1/stats/burden_treemap
GET  /v1/wellness/articles                                    # list
GET  /v1/wellness/articles/{slug}                             # one
GET  /v1/health
GET  /v1/version
GET  /openapi.json
GET  /docs
```

All errors are RFC 7807 problem-details. CORS allow-list pinned to the Vercel domain. SlowAPI rate limit 30 req/min/IP. Structured JSON logs (loguru). Optional `X-API-Key` header gated by env var. Prometheus metrics at `/metrics`.

---

## 13. File structure

```
medxai/
├── .github/workflows/             ci.yml, docs.yml, deploy-spaces.yml, release.yml
├── .dvc/
├── .pre-commit-config.yaml
├── pyproject.toml
├── uv.lock
├── Makefile                        setup / lint / test / train / eval / app / docs / paper
├── README.md                       short, links to docs
├── MEDXAI_PROMPT.md                this file
├── LICENSE                         MIT
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .env.example
├── docker-compose.yml
├── docker/
│   ├── api.Dockerfile
│   └── streamlit.Dockerfile
├── configs/
│   ├── data/
│   ├── model/
│   ├── train/
│   ├── xai/
│   ├── reference_ranges/           cited reference ranges as YAML
│   └── experiment/
├── data/                           DVC-tracked, gitignored
│   ├── raw/ interim/ processed/ synthetic/
├── content/
│   └── wellness/                   one .md per article (front-matter + body)
├── notebooks/                      EDA + paper figures
├── src/medxai/
│   ├── data/                       datamodules + synthetic generators
│   ├── models/
│   │   ├── vision/  tabular/
│   │   └── registry.py
│   ├── training/                   trainer_vision.py / trainer_tabular.py / losses.py
│   ├── evaluation/                 metrics, calibration, fairness, robustness, significance
│   ├── xai/
│   │   ├── vision/                 gradcam, gradcam_pp, integrated_gradients, occlusion
│   │   ├── tabular/                shap, lime, counterfactual
│   │   ├── faithfulness.py
│   │   └── sanity_checks.py
│   ├── guidance/                   engine + rules/*.yaml + disclaimers.py
│   ├── lab/                        cbc, urinalysis, lipid rule engines
│   ├── wellness/                   loader for content/wellness/*.md
│   ├── viz/                        single source for chart specs
│   ├── reports/                    PDF builder + templates
│   ├── api/                        FastAPI app, routers, schemas
│   └── utils/                      seeding, logging, io
├── streamlit_app/
│   ├── Home.py
│   ├── pages/                      one file per page from Section 11.5
│   └── components/
├── frontend/                       Next.js 14 app
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── tailwind.config.ts
├── tests/
│   ├── unit/  integration/  property/  e2e/  visual/
│   └── conftest.py
├── scripts/
│   ├── download_data.py
│   ├── prepare_splits.py
│   ├── generate_synthetic_cbc.py
│   ├── generate_synthetic_urinalysis.py
│   ├── train.py                    python -m scripts.train experiment=...
│   ├── evaluate.py
│   ├── export_model.py             TorchScript / ONNX
│   └── make_paper_figures.py
├── docs/                           MkDocs Material site
│   ├── index.md
│   ├── architecture.md
│   ├── getting_started.md
│   ├── datasheets/
│   ├── model_cards/
│   ├── xai_methodology.md
│   ├── evaluation.md
│   ├── ethics_and_limitations.md
│   ├── reproducibility.md
│   ├── decisions/                  ADRs
│   └── api_reference.md            mkdocstrings auto
├── reports/
│   ├── paper/                      LaTeX, IEEE template
│   ├── slides/                     defense.pdf
│   └── figures/medxai.mplstyle
└── benchmarks/runtime.md
```

This is the spec. Don't add new top-level dirs without proposing them first.

---

## 14. CI/CD

`.github/workflows/ci.yml` on every PR:

1. Setup uv with cache.
2. `uv sync --all-extras`.
3. `ruff check . && ruff format --check .`.
4. `mypy src/`.
5. `pytest -q --cov=src/medxai --cov-fail-under=80`.
6. **Wellness Atlas linter** — fails if any article has < 2 citations or is missing the disclaimer.
7. **Theme linter** — fails if any forbidden token (`bg-black`, `bg-zinc-900`, dark-mode-only patterns) appears in `frontend/` or `streamlit_app/`.
8. Smoke training (`fast_dev.yaml`, 1 epoch, 32 samples) to catch breakage.
9. Build Docker images (no push).

Other workflows:
- `docs.yml` — build MkDocs, deploy to GH Pages on `main`.
- `deploy-spaces.yml` — on tag `v*`, push Streamlit and FastAPI dirs to HF Spaces via `huggingface_hub`.
- `release.yml` — semantic-release version bump + changelog.

`.pre-commit-config.yaml`: ruff, mypy, end-of-file-fixer, trailing-whitespace, check-yaml/toml, detect-secrets, nbstripout.

---

## 15. Testing

- **Unit:** every pure function in `src/medxai/`.
- **Integration:** end-to-end predict + explain on a 10-image fixture set per modality.
- **Property (hypothesis):** preprocessing functions are idempotent on already-preprocessed inputs; metric functions return values in `[0, 1]`; rule engine never emits the verb "diagnose" (`assert "diagnose" not in suggestion.text.lower()`).
- **Snapshot:** API responses against `tests/snapshots/`.
- **Visual regression** (Playwright + pixelmatch on key Next.js pages) — catches the homepage breaking silently.
- **E2E (Playwright):** upload an image on Streamlit and Next.js, verify a result appears.
- **Coverage gate:** 80 % on `src/medxai/`.

---

## 16. Documentation (MkDocs Material)

- `index.md` — pitch + screenshots + quickstart.
- `getting_started.md` — clone → `make setup` → `make demo` in <5 minutes.
- `architecture.md` — Section 7 diagram + Mermaid sequence diagrams for predict and explain.
- `datasheets/<dataset>.md` — Gebru-style.
- `model_cards/<model>.md` — Mitchell-style.
- `xai_methodology.md` — methods, when each fails, faithfulness metrics, sanity checks.
- `evaluation.md` — every metric and plot with formulas.
- `ethics_and_limitations.md` — bias, dataset shift, dual-use, who should NOT use this.
- `reproducibility.md` — seeds, env, hardware, exact commands.
- `decisions/` — ADRs.
- `api_reference.md` — auto from docstrings.

README.md (top level) — short: 30-second pitch, hero GIF, disclaimer, quickstart in 4 commands, architecture diagram, results table with bootstrapped CIs, citation block, license.

---

## 17. Research artifacts — what turns this into "MSc-grade"

- **Paper** in `reports/paper/`: IEEE template, 6–8 pages — motivation, related work (CheXNet, DenseNet-CXR, SHAP, Captum, Adebayo et al., model cards), method, datasets, experiments, XAI faithfulness analysis, limitations, conclusion. `make paper` builds the PDF.
- **Slides** (`reports/slides/defense.pdf`): 10–15 slides for a 15-minute defense.
- **Model cards** for every shipped model. **Datasheets** for every dataset.
- **Reproducibility statement** at the end of the paper.
- **Ablations:** backbone comparison, with/without augmentation, with/without calibration, XAI faithfulness across methods.
- **Statistical tests:** McNemar between top two models per task; bootstrapped CIs everywhere.

---

## 18. Deployment

| Component | Where |
|---|---|
| FastAPI backend | HuggingFace Spaces (Docker SDK) |
| Streamlit demo | HuggingFace Spaces (Streamlit SDK) — calls the FastAPI Space |
| Next.js frontend | Vercel — env var points to the FastAPI Space |
| Docs (MkDocs) | GitHub Pages |
| Model artifacts | HF Hub (one repo per model, model card auto-published) |
| Datasets / splits | DVC remote on Google Drive |
| Tracking | MLflow local in dev; optional Dagshub remote |

Every deploy is GitHub-Actions-only. Tagged release builds and pushes everywhere.

---

## 19. Performance budget (per request, on free-tier HF Space CPU)

- Image predict + explain: < 6 s end to end. If a model can't make it, downscale or quantize.
- Tabular predict + SHAP: < 1 s.
- Homepage cold load on Vercel: < 2.5 s LCP on a mid-range mobile.
- API JSON payload < 1 MB; image payloads streamed, never base64-bloated when avoidable.

---

## 20. Phased plan — Claude executes phase by phase

For each phase: (a) restate scope, (b) implement, (c) tests pass, (d) commit, (e) summarize, (f) wait for "go".

### Phase 0 — Scaffolding
Repo init, `pyproject.toml`, `uv.lock`, pre-commit, ruff/mypy. Empty `src/medxai/` with version stamp. CI green. README skeleton, license, disclaimer. MkDocs skeleton. `Makefile` with the standard targets. docker-compose with api + streamlit + jupyter on the same image. Theme tokens locked in `streamlit_app/.streamlit/config.toml` and `frontend/tailwind.config.ts`.

**Done when:** `make setup && make test` is green on a fresh clone.

### Phase 1 — Data layer
DVC init + remote. `scripts/download_data.py` for all five Tier-1 imaging datasets and all eight tabular datasets. Synthetic CBC + urinalysis generators with cited reference ranges. DataModule classes + deterministic splits (CSV of indices, hashed). EDA notebooks for at least WDBC and Kermany. Datasheets for every Tier-1 dataset.

### Phase 2 — Tabular MVP (proof the loop works end to end)
Train LR / RF / XGBoost on WDBC. MLflow up. Full eval (metrics, calibration, bootstrapped CIs). TreeSHAP + LIME + DiCE. Model card v1. Streamlit page that loads WDBC and explains a prediction end to end. **PDF report endpoint working on this single task.**

**Milestone:** paste 30 features → prediction + SHAP + counterfactual + guidance + PDF. The whole loop is real before any image model exists.

### Phase 3 — Vision MVP
Train DenseNet121 on Kermany Pediatric. Grad-CAM + Integrated Gradients. Faithfulness metrics. Adebayo sanity checks. Streamlit Chest-X-ray page live.

### Phase 4 — Scale up vision
ChestX-ray14 multi-label. Backbone comparison (DenseNet / EfficientNet / one ViT). CBIS-DDSM mammography patches. HAM10000 derm. APTOS DR. All Streamlit image pages live.

### Phase 5 — Remaining tabular + lab
Pima, Heart, Liver, CKD, Stroke, Parkinson's, Thyroid — full pipelines and model cards. CBC, urinalysis, lipid rule engines + their Streamlit pages.

### Phase 6 — Wellness Atlas
Write all 10 articles in `content/wellness/*.md` with two-citation minimum. Render in Streamlit and Next.js. Wellness CI linter live.

### Phase 7 — API + Next.js
FastAPI backend feature-complete. Pydantic schemas. OpenAPI live. Next.js frontend on Vercel calling the API. Polished homepage charts. PDF report endpoint integrated.

### Phase 8 — Deploy + docs + paper
HF Spaces for Streamlit and FastAPI. Vercel for Next.js. MkDocs on GH Pages. Paper compiled. Slides committed. v1.0.0 tagged.

### Phase 9 — Polish
Demo GIF / 30-second screencast on the README. Re-read the repo as a hostile reviewer; file issues; close them. Final ethics & limitations pass.

---

## 21. Definition of "done" for the whole project

A reviewer at TUM / RWTH / Heidelberg / TU Berlin / LMU should be able to:

1. Click the live Vercel URL → land on a polished white-themed homepage → run a prediction with explanation in under 60 seconds.
2. Clone the repo → `make setup && make demo` → reach the same state locally in under 10 minutes.
3. Open `docs/` and find a coherent story: what, why, how, with what data, with what limits.
4. Open `reports/paper/main.pdf` and read 6 pages that look like research, not a tutorial.
5. Open `content/wellness/` and find ten properly-cited articles.
6. Open the GitHub Actions tab and see green CI runs going back to the first commit.

If any of those six fail, the project is not done.

---

## 22. Specific instructions for THIS Claude Code session

1. First action: read this file end to end, then write `docs/PLAN.md` exactly as Section 0 specifies. Stop. Wait.
2. After "go", begin Phase 0 only. Commit with `chore(scaffold): initialize project structure` when CI is green. Show the diff summary.
3. No placeholder weights, no fake metrics, no fabricated screenshots. If something needs a GPU and we're on CPU, say so — we'll either reduce scope or run it on Colab/Kaggle and pull artifacts back.
4. Architecture-changing question → stop and ask. Style call → decide and log an ADR in `docs/decisions/`.
5. Tests with the code, not after. Untested function → not committed.
6. After every phase, append a phase note to `CHANGELOG.md` under `## [Unreleased]`.
7. Never `git push --force` on `main`. Branch and PR for anything bigger than a typo.
8. If this document conflicts with reality, update **this document** in the same PR that handles the change.

---

## 23. Stretch goals (only after Phase 8 is green)

- ViT attention rollout vs CNN Grad-CAM head-to-head.
- Multi-modal fusion: image + tabular for one condition (e.g., breast cancer with mammogram patch + WDBC features).
- Active-learning loop on the synthetic data.
- A small report-text parser (BioBERT/ClinicalBERT) that extracts structured findings from pasted lab-report text.
- Federated-learning toy demo with Flower across two simulated clients on WDBC.

These are explicitly optional and labeled as such in the README so reviewers see scope discipline, not feature creep.

---

## 24. Final note to Claude

Build this like someone whose name is on the front page of the repo for the next two years and whose admission to a top German MSc partly depends on it — because that is true. Be opinionated about quality. Push back if I ask for something that would damage the project. Every commit should be one a hiring committee or admissions reviewer is glad to read.

Begin with Section 0 / step 1.
