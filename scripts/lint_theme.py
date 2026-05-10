"""Theme linter — enforce the locked white theme from MEDXAI_PROMPT.md Section 11.

Run as a script:

    uv run python -m scripts.lint_theme              # scan default targets
    uv run python -m scripts.lint_theme path/to/dir  # scan an explicit path

Exit codes:
    0  — clean (no forbidden tokens found)
    1  — at least one forbidden token found (CI-fail)
    2  — usage / IO error

The forbidden-token list comes from spec Section 11.3:
"CI fails the build if any of those strings appear in `frontend/`."
We extend the rule to ``streamlit_app/`` for symmetry — both surfaces
must look identical.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

# Default scan roots — relative to repo root.
DEFAULT_TARGETS: tuple[str, ...] = ("frontend", "streamlit_app")

# File extensions worth scanning. Anything binary is ignored by extension.
SCANNED_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".mjs",
        ".cjs",
        ".css",
        ".scss",
        ".sass",
        ".html",
        ".mdx",
        ".md",
        ".py",
        ".toml",
        ".json",
        ".yaml",
        ".yml",
    }
)

# Directories that should never be scanned even if they live under a target.
SKIP_DIR_NAMES: frozenset[str] = frozenset(
    {
        "node_modules",
        ".next",
        "out",
        "dist",
        "build",
        "__pycache__",
        ".venv",
        ".git",
        ".turbo",
        ".cache",
    }
)

# Each rule = (pattern, human message). Patterns are compiled case-insensitive.
# Keep the rules narrow: they should catch real dark-mode patterns, not flag
# legitimate uses of the word "dark" in prose (which is why we anchor on the
# Tailwind/CSS class form).
FORBIDDEN_RULES: tuple[tuple[str, str], ...] = (
    (r"\bbg-black\b", "forbidden Tailwind class `bg-black`"),
    (r"\bbg-zinc-900\b", "forbidden Tailwind class `bg-zinc-900`"),
    (r"\bbg-zinc-800\b", "forbidden Tailwind class `bg-zinc-800`"),
    (r"\bbg-neutral-900\b", "forbidden Tailwind class `bg-neutral-900`"),
    (r"\bbg-slate-900\b", "forbidden Tailwind class `bg-slate-900`"),
    (r"\bbg-gray-900\b", "forbidden Tailwind class `bg-gray-900`"),
    (r"\bdark:bg-", "forbidden Tailwind dark-mode-only utility `dark:bg-...`"),
    (r"\bdark:text-", "forbidden Tailwind dark-mode-only utility `dark:text-...`"),
    (
        r"darkMode\s*:\s*['\"](class|media|selector)['\"]",
        "forbidden Tailwind config — `darkMode` must not be set",
    ),
)


@dataclass(frozen=True, slots=True)
class Finding:
    path: Path
    line_no: int
    line: str
    rule: str

    def format(self) -> str:
        return f"{self.path}:{self.line_no}: {self.rule}\n    {self.line.rstrip()}"


def iter_files(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.suffix.lower() not in SCANNED_EXTENSIONS:
                continue
            yield path


def scan_file(path: Path, compiled_rules: Sequence[tuple[re.Pattern[str], str]]) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        # Non-text or unreadable file — skip silently. The directory walker
        # already filters by extension, so reaching here is unusual.
        return findings
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern, message in compiled_rules:
            if pattern.search(line):
                findings.append(Finding(path=path, line_no=line_no, line=line, rule=message))
    return findings


def lint(roots: Sequence[Path]) -> list[Finding]:
    compiled = tuple((re.compile(p, re.IGNORECASE), msg) for p, msg in FORBIDDEN_RULES)
    findings: list[Finding] = []
    for f in iter_files(roots):
        findings.extend(scan_file(f, compiled))
    return findings


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lint_theme",
        description="Fail CI if forbidden dark-mode tokens appear in UI source.",
    )
    p.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help=f"Directories to scan. Defaults to: {', '.join(DEFAULT_TARGETS)}.",
    )
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    roots: Sequence[Path] = (
        [p.resolve() for p in args.paths]
        if args.paths
        else [(repo_root / t).resolve() for t in DEFAULT_TARGETS]
    )

    findings = lint(roots)

    if not findings:
        scanned = ", ".join(
            str(r.relative_to(repo_root)) if r.is_relative_to(repo_root) else str(r)
            for r in roots
            if r.exists()
        )
        print(f"theme-linter: clean — scanned {scanned or '(no roots existed)'}")
        return 0

    print(f"theme-linter: {len(findings)} forbidden token(s) found:\n", file=sys.stderr)
    for f in findings:
        print(f.format(), file=sys.stderr)
    print(
        "\nSee MEDXAI_PROMPT.md Section 11.1 / 11.3 — the visual theme is "
        "locked white. No dark mode in v1.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
