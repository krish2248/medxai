# MedXAI — documentation

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions. If you have a medical concern, consult a licensed clinician.**

MedXAI is a multi-modal medical AI portfolio system that pairs a curated set
of imaging, tabular, and lab-report models with quantitative explainability
(Grad-CAM, Integrated Gradients, SHAP, LIME, DiCE) and a human-curated,
citation-backed Wellness Atlas of preventive-health knowledge.

This documentation site is built phase by phase alongside the code. The
authoritative specification lives in
[`MEDXAI_PROMPT.md`](https://github.com/krish2248/medxai/blob/main/MEDXAI_PROMPT.md);
the phased plan is in [`PLAN.md`](PLAN.md).

## What lives here

| Section | Purpose | Status |
|---|---|---|
| [Getting started](getting_started.md) | Install, sync, run lint + tests | Phase 0 |
| [Architecture](architecture.md) | System diagram, component responsibilities | Phase 0 (sketch) |
| [Plan](PLAN.md) | Restatement, assumptions, open questions, commit plan | Phase 0 |
| Decisions (`decisions/`) | Architecture Decision Records | Phase 0+ |
| Datasheets | Gebru-style per dataset | Phase 1+ |
| Model cards | Mitchell-style per model | Phase 2+ |
| XAI methodology | Methods, faithfulness, sanity checks | Phase 3+ |
| Evaluation | Metrics + plots with formulas | Phase 2+ |
| Reproducibility | Seeds, env, hardware, exact commands | Phase 2+ |
| Ethics & limitations | Bias, dataset shift, dual-use | Phase 8+ |
| API reference | Auto-generated from docstrings | Phase 7+ |

## License

[MIT](https://github.com/krish2248/medxai/blob/main/LICENSE).
