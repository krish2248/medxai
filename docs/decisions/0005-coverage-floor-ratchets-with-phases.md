---
id: 0005
title: Coverage floor ratchets up with phases
status: accepted
date: 2026-05-10
phase: 0
---

# 0005 — Coverage floor ratchets up with phases

## Context

`MEDXAI_PROMPT.md` Section 14 step 5 mandates **80% coverage on
`src/medxai/`** in CI. In Phase 0 there is essentially no production code
(`src/medxai/__init__.py` is the version stamp), so a literal 80% gate
either trivially passes (one tested function = 100%) or — more dangerously
— silently passes on tiny denominators that would mask real regressions
when real code lands.

## Decision

Coverage `fail_under` ratchets up phase by phase:

| Phase | `fail_under` | Reason |
|---|---|---|
| 0 | 0  | Only `__init__.py` + linters in `scripts/`; nothing meaningful in `src/medxai/` to measure yet. |
| 1 | 60 | Datamodules + synthetic generators add real branches. |
| 2 | 75 | First real model + eval + XAI module. |
| 3+ | 80 | Hits the spec target and stays there. |

Each phase's PR that increases the floor must also explain *why* the
codebase now supports the higher gate.

## Consequences

- **Positive:** No false sense of security from 100% coverage on five
  lines in Phase 0.
- **Positive:** Spec target (80%) is met by Phase 3 — well before any
  shipped model.
- **Negative:** Slightly more bookkeeping. Mitigation: this ADR + the
  `fail_under` value lives in `pyproject.toml` so it is always visible.

## Status

Accepted at the start of Phase 0.
