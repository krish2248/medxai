# Architecture

> Phase 0 stub. The full diagram + Mermaid sequence diagrams (Section 16 of
> the spec) land alongside the API in Phase 7.

## Target topology

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

Streamlit ships first and is what reviewers click. Next.js is the polished
surface. **Both call the same FastAPI backend** — there is one canonical
inference path per modality.

## Module map

| Layer | Package | Phase added |
|---|---|---|
| Models — vision | `src/medxai/models/vision/` | 3 |
| Models — tabular | `src/medxai/models/tabular/` | 2 |
| Datamodules | `src/medxai/data/` | 1 |
| Training | `src/medxai/training/` | 2 |
| Evaluation | `src/medxai/evaluation/` | 2 |
| XAI — vision | `src/medxai/xai/vision/` | 3 |
| XAI — tabular | `src/medxai/xai/tabular/` | 2 |
| Guidance engine | `src/medxai/guidance/` | 2 |
| Lab interpreters | `src/medxai/lab/` | 5 |
| Wellness loader | `src/medxai/wellness/` | 6 |
| Visualisation | `src/medxai/viz/` | 5 |
| PDF reports | `src/medxai/reports/` | 2 |
| FastAPI app | `src/medxai/api/` | 7 |
