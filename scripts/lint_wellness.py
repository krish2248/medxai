"""Wellness Atlas linter — citation count + disclaimer presence.

Per MEDXAI_PROMPT.md Section 14 step 6: CI fails if any article in
``content/wellness/`` has fewer than two citations or is missing the
standard disclaimer.

Phase 0 ships the linter as an empty-directory no-op so the CI step is
wired up from day one. Phase 6 will populate ``content/wellness/`` with
the ten articles from Section 4.1, and the same script will then enforce
the rules for real.

Run as a script:

    uv run python -m scripts.lint_wellness

Exit codes:
    0  — clean (or directory empty)
    1  — at least one article violates the rules
    2  — usage / IO error
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONTENT_DIR = Path("content/wellness")
MIN_CITATIONS = 2

# Section 11.4 — the verbatim disclaimer text. The rule below uses a
# stable substring (not the whole paragraph) so trivial whitespace edits
# don't break the check; we still require the distinctive phrase.
DISCLAIMER_MARKER = "is not a medical device"


@dataclass(frozen=True, slots=True)
class ArticleViolation:
    path: Path
    reason: str

    def format(self) -> str:
        return f"{self.path}: {self.reason}"


def _load_article(path: Path) -> dict[str, object]:
    """Load a wellness article. Articles are YAML-front-matter + markdown body.

    For Phase 0 the simplest round-trip is YAML for the metadata and the
    raw text for the disclaimer presence check. We accept both ``.md``
    (front-matter delimited by ``---``) and pure ``.yaml``/``.yml`` to
    keep early authoring friction low; Phase 6 will tighten this to MDX.
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        loaded = yaml.safe_load(text) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"{path}: top-level YAML is not a mapping")
        return loaded

    # Markdown with YAML front matter delimited by `---`.
    if text.startswith("---"):
        _, _, rest = text.partition("---")
        front, _, body = rest.partition("---")
        meta = yaml.safe_load(front) or {}
        if not isinstance(meta, dict):
            raise ValueError(f"{path}: front-matter is not a mapping")
        meta["__body__"] = body
        return meta

    return {"__body__": text}


def lint_article(path: Path) -> list[ArticleViolation]:
    violations: list[ArticleViolation] = []
    try:
        data = _load_article(path)
    except (yaml.YAMLError, ValueError, OSError) as exc:
        return [ArticleViolation(path=path, reason=f"could not parse: {exc}")]

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) < MIN_CITATIONS:
        violations.append(
            ArticleViolation(
                path=path,
                reason=(
                    f"requires >= {MIN_CITATIONS} citations under `sources:`, "
                    f"found {len(sources) if isinstance(sources, list) else 0}"
                ),
            )
        )

    body = str(data.get("__body__", ""))
    disclaimer_field = str(data.get("disclaimer", ""))
    if (
        DISCLAIMER_MARKER not in body
        and DISCLAIMER_MARKER not in disclaimer_field
        and disclaimer_field.strip().lower() != "standard"
    ):
        violations.append(
            ArticleViolation(
                path=path,
                reason=(
                    "missing the standard disclaimer (Section 11.4). Either "
                    "set `disclaimer: standard` or include the verbatim text."
                ),
            )
        )

    return violations


def lint(content_dir: Path) -> list[ArticleViolation]:
    if not content_dir.exists():
        return []
    articles = sorted(
        p for p in content_dir.rglob("*") if p.suffix.lower() in {".md", ".mdx", ".yaml", ".yml"}
    )
    violations: list[ArticleViolation] = []
    for article in articles:
        violations.extend(lint_article(article))
    return violations


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lint_wellness",
        description="Fail CI if any Wellness Atlas article has < 2 citations or no disclaimer.",
    )
    p.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=None,
        help=f"Path to scan. Defaults to repo-root/{DEFAULT_CONTENT_DIR}.",
    )
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    target = args.path.resolve() if args.path else (repo_root / DEFAULT_CONTENT_DIR).resolve()

    violations = lint(target)

    if not target.exists():
        print(f"wellness-linter: {target} does not exist yet — Phase 6 will populate it. OK.")
        return 0

    if not violations:
        print(f"wellness-linter: clean — checked {target}")
        return 0

    print(f"wellness-linter: {len(violations)} violation(s) found:\n", file=sys.stderr)
    for v in violations:
        print(v.format(), file=sys.stderr)
    print(
        "\nSee MEDXAI_PROMPT.md Section 4.2 / 4.4 / 11.4 for the article schema,"
        " citation rules, and disclaimer text.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
