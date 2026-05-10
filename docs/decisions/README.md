# Architecture Decision Records (ADRs)

Per `MEDXAI_PROMPT.md` Section 22, *style calls* are made by the engineer
and recorded here as ADRs. *Architecture-changing* questions stop and ask
the user instead.

Each ADR has the following frontmatter:

```yaml
id: 0001
title: ...
status: proposed | accepted | deprecated | superseded by 0002
date: YYYY-MM-DD
phase: 0..9
```

Format follows Michael Nygard's "Documenting Architecture Decisions" — short,
context → decision → consequences. ADRs are immutable once accepted; if a
later decision overrides an earlier one, write a new ADR with
`status: superseded by 000X` and link both ways.

## Index

| ID | Title | Status |
|---|---|---|
| [0001](0001-cross-platform-make.md) | Cross-platform Make wrapper for Windows | accepted |
| [0002](0002-defer-frontend-scaffold-to-phase-7.md) | Defer Next.js scaffold to Phase 7 | accepted |
| [0003](0003-defer-wandb-dagshub.md) | Skip W&B and Dagshub in v1 | accepted |
| [0004](0004-defer-dvc-remote-and-hf-hub.md) | Defer DVC remote and HF Hub setup | accepted |
| [0005](0005-coverage-floor-ratchets-with-phases.md) | Coverage floor ratchets with phases | accepted |
