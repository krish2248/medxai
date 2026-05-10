---
id: 0001
title: Cross-platform Make wrapper for Windows
status: accepted
date: 2026-05-10
phase: 0
---

# 0001 — Cross-platform Make wrapper for Windows

## Context

`MEDXAI_PROMPT.md` Section 13 prescribes a `Makefile` with standard targets
(`setup`, `lint`, `test`, `train`, `eval`, `app`, `docs`, `paper`). The
project's primary developer works on Windows 11 with PowerShell as the
default shell. Vanilla `make` is not installed on stock Windows.

The choices considered:

1. **Require WSL.** Forces a Linux subsystem install on every Windows
   contributor; alien to non-experts and complicates IDE setup.
2. **Require Chocolatey/Scoop `make`.** Adds another out-of-band install
   step; subtly different `make` behaviour on Windows when paths contain
   spaces.
3. **Ship a parallel `make.ps1`.** Mirrors every target as a PowerShell
   `switch`. Both files delegate to the same `uv run …` commands, so the
   POSIX `make` and PowerShell flows are observably identical.

## Decision

Ship **both** `Makefile` (POSIX) and `make.ps1` (PowerShell). Targets are
1:1. CI uses `make` (Linux runners). Local Windows users invoke
`./make.ps1 <target>`. Every spec sentence of the form *"`make X`"* should
be read as *"`make X` (POSIX) or `./make.ps1 X` (PowerShell)"*.

Both files are thin wrappers — the actual command logic lives in `uv run …`
invocations, so divergence is structurally limited.

## Consequences

- **Positive:** No mandatory WSL install for Windows users. Spec command
  surface stays as written. CI behaviour is unchanged.
- **Positive:** Adding a target requires editing two files; the doubled
  surface is small and is caught by code review.
- **Negative:** Two files to keep in sync. Mitigation: keep them mechanical
  wrappers around `uv run …`; if logic ever needs to live somewhere, it
  belongs in `scripts/` (one Python source of truth).
- **Negative:** PowerShell scripts are blocked by execution policy on some
  locked-down machines. Documented workaround in README later:
  `powershell -ExecutionPolicy Bypass -File .\make.ps1 <target>`.

## Status

Accepted at the start of Phase 0.
