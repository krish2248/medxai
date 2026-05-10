---
id: 0003
title: Skip W&B and Dagshub in v1
status: accepted
date: 2026-05-10
phase: 0
---

# 0003 — Skip Weights & Biases and Dagshub in v1

## Context

`MEDXAI_PROMPT.md` Section 6 lists MLflow as the primary tracker and
labels W&B as "optional if I add a key"; Section 18 lists Dagshub as
"optional remote." Both add account-management overhead and external
dependencies.

## Decision

For the v1.0.0 release covered by Phases 0–9, use **MLflow local** only.
No W&B, no Dagshub. The `MLFLOW_TRACKING_URI` env var (defaulting to
`./mlruns`) is the only knob; switching to a remote MLflow / Dagshub later
is a one-line change.

## Consequences

- **Positive:** No third-party accounts required to run the project end
  to end on a fresh machine.
- **Positive:** Reproducibility statement (Section 8.4) only needs to
  cite the local MLflow run directory + git SHA.
- **Negative:** Cross-machine experiment comparison is harder. Acceptable
  for a solo project on a fixed cadence.

Revisit if the user later wants to share dashboards with reviewers — at
that point, switch to a remote MLflow on Dagshub (free tier).

## Status

Accepted at the start of Phase 0.
