---
id: 0002
title: Defer full Next.js scaffold to Phase 7
status: accepted
date: 2026-05-10
phase: 0
---

# 0002 — Defer full Next.js scaffold to Phase 7

## Context

`MEDXAI_PROMPT.md` Sections 5, 11, and 13 describe a polished Next.js 14
frontend with a Tailwind theme, shadcn/ui components, and a Plotly-driven
dashboard. Section 20's Phase 7 is where the API + Next.js are
implemented; Phase 0 only mandates that the **theme tokens** are locked.

Running `pnpm create next-app` in Phase 0 would pull `node_modules`,
`.next`, and a frontend test runner into a repo that has nothing to render.
That bloats CI, adds a Node toolchain dependency to Phase 0, and creates
many "TODO" frontend files that the spec forbids on `main`.

## Decision

In Phase 0, scaffold only the files needed for the **theme linter** to do
its job:

- `frontend/tailwind.config.ts` — locked palette, fonts, shadows from
  Section 11.1.
- `frontend/app/globals.css` — CSS variables matching the same tokens.
- `frontend/.gitkeep` (effectively the directory marker).

Do **not** install Node, run `pnpm create next-app`, or commit
`package.json` until Phase 7. CI does not run any Node tooling in Phase 0.

## Consequences

- **Positive:** Theme is locked from day one — the linter (Section 14
  step 7) has real files to scan, and any future PR that introduces
  `bg-black` is rejected immediately.
- **Positive:** Phase 0 CI stays Python-only and fast.
- **Negative:** The `frontend/` directory looks empty until Phase 7. Risk
  mitigated by README + this ADR explaining why.

## Status

Accepted at the start of Phase 0.
