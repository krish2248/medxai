---
id: 0004
title: Defer DVC remote and HuggingFace Hub setup
status: accepted
date: 2026-05-10
phase: 0
---

# 0004 — Defer DVC remote and HuggingFace Hub setup

## Context

`MEDXAI_PROMPT.md` Section 13 reserves a `.dvc/` directory and Section 18
specifies a Google Drive DVC remote and one HF Hub repo per shipped model.
Both require credential setup (Google OAuth, HF token) that is unrelated
to the Phase 0 acceptance criteria.

## Decision

- **Phase 0:** do not run `dvc init` and do not create HF Hub repos. The
  `.gitignore` already reserves `.dvc/cache` so a future `dvc init` is
  trivial.
- **Phase 1 (data layer):** `dvc init`, configure the Google Drive
  remote, write the credentials section of `docs/getting_started.md`.
- **Phase 8 (deploy):** create one HF Hub repo per shipped model, push
  weights + auto-published model card.

## Consequences

- **Positive:** Phase 0 has no out-of-band credential setup; a fresh
  contributor can `make setup` with no Kaggle/Google/HF tokens.
- **Negative:** Anyone who tries `dvc pull` in Phase 0 gets an error.
  Mitigation: README's quickstart in Phase 0 does not mention DVC.

## Status

Accepted at the start of Phase 0.
