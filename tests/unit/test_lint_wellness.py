"""Tests for ``scripts.lint_wellness``."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.lint_wellness import ArticleViolation, lint, lint_article, main


def _write_article(path: Path, *, sources: int, disclaimer: str = "standard") -> None:
    src_yaml = "\n".join(
        f"  - title: Source {i}\n    url: https://example.org/{i}\n    org: WHO\n    year: 2024\n    tier: 1"
        for i in range(sources)
    )
    body = (
        "---\n"
        "slug: demo-article\n"
        "title: Demo article\n"
        f"sources:\n{src_yaml or '  []'}\n"
        f"disclaimer: {disclaimer}\n"
        "---\n"
        "Body goes here.\n"
    )
    path.write_text(body, encoding="utf-8")


def test_missing_directory_is_clean(tmp_path: Path) -> None:
    assert lint(tmp_path / "does-not-exist") == []


def test_empty_directory_is_clean(tmp_path: Path) -> None:
    assert lint(tmp_path) == []


def test_article_with_two_sources_passes(tmp_path: Path) -> None:
    article = tmp_path / "demo.md"
    _write_article(article, sources=2)
    assert lint_article(article) == []


def test_article_with_one_source_fails(tmp_path: Path) -> None:
    article = tmp_path / "demo.md"
    _write_article(article, sources=1)
    violations = lint_article(article)
    assert len(violations) == 1
    assert "citation" in violations[0].reason


def test_article_missing_disclaimer_fails(tmp_path: Path) -> None:
    article = tmp_path / "demo.md"
    _write_article(article, sources=2, disclaimer="ignored")
    violations = lint_article(article)
    assert any("disclaimer" in v.reason for v in violations)


def test_article_with_inline_disclaimer_passes(tmp_path: Path) -> None:
    body = (
        "---\n"
        "slug: demo\n"
        "title: Demo\n"
        "sources:\n"
        "  - title: A\n    url: https://a\n    org: WHO\n    year: 2024\n    tier: 1\n"
        "  - title: B\n    url: https://b\n    org: CDC\n    year: 2024\n    tier: 1\n"
        "disclaimer: ''\n"
        "---\n"
        "MedXAI is not a medical device.\n"
    )
    article = tmp_path / "demo.md"
    article.write_text(body, encoding="utf-8")
    assert lint_article(article) == []


def test_unparseable_yaml_is_reported(tmp_path: Path) -> None:
    article = tmp_path / "broken.md"
    article.write_text("---\n: : :\n---\nbody\n", encoding="utf-8")
    violations = lint_article(article)
    assert len(violations) == 1
    assert "could not parse" in violations[0].reason


def test_main_returns_0_on_missing_dir(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "nope")]) == 0
    assert "Phase 6" in capsys.readouterr().out


def test_main_returns_1_on_violation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_article(tmp_path / "bad.md", sources=0)
    assert main([str(tmp_path)]) == 1
    assert "violation" in capsys.readouterr().err


def test_main_returns_0_on_clean_dir(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_article(tmp_path / "ok.md", sources=2)
    assert main([str(tmp_path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_violation_format_contains_path_and_reason() -> None:
    v = ArticleViolation(path=Path("a/b.md"), reason="r")
    assert "b.md" in v.format() and "r" in v.format()
