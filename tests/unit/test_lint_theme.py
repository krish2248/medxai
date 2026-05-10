"""Tests for ``scripts.lint_theme``."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from scripts.lint_theme import FORBIDDEN_RULES, Finding, lint, main


def test_clean_directory_is_clean(tmp_path: Path) -> None:
    (tmp_path / "ok.tsx").write_text(
        'export const x = <div className="bg-white text-text-primary">hi</div>;\n',
        encoding="utf-8",
    )
    assert lint([tmp_path]) == []


def test_bg_black_is_flagged(tmp_path: Path) -> None:
    bad = tmp_path / "bad.tsx"
    bad.write_text(
        'export const x = <div className="bg-black">nope</div>;\n',
        encoding="utf-8",
    )
    findings = lint([tmp_path])
    assert len(findings) == 1
    assert findings[0].path == bad
    assert findings[0].line_no == 1
    assert "bg-black" in findings[0].rule


def test_dark_prefix_is_flagged(tmp_path: Path) -> None:
    (tmp_path / "card.tsx").write_text(
        'export const x = <div className="bg-white dark:bg-zinc-900">x</div>;\n',
        encoding="utf-8",
    )
    findings = lint([tmp_path])
    # Two rules trigger here: `bg-zinc-900` and `dark:bg-`. Both are real.
    assert {f.rule for f in findings} == {
        "forbidden Tailwind class `bg-zinc-900`",
        "forbidden Tailwind dark-mode-only utility `dark:bg-...`",
    }


def test_tailwind_darkmode_config_is_flagged(tmp_path: Path) -> None:
    (tmp_path / "tailwind.config.ts").write_text(
        'export default { darkMode: "class", content: [] };\n',
        encoding="utf-8",
    )
    findings = lint([tmp_path])
    assert any("darkMode" in f.rule for f in findings)


def test_skips_node_modules(tmp_path: Path) -> None:
    nm = tmp_path / "node_modules" / "evil"
    nm.mkdir(parents=True)
    (nm / "x.tsx").write_text(
        'export const x = <div className="bg-black">nope</div>;\n',
        encoding="utf-8",
    )
    assert lint([tmp_path]) == []


def test_skips_unscanned_extensions(tmp_path: Path) -> None:
    (tmp_path / "image.png").write_text("bg-black", encoding="utf-8")
    assert lint([tmp_path]) == []


def test_main_returns_0_on_clean_path(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "ok.css").write_text("body { background: #FFFFFF; }\n", encoding="utf-8")
    assert main([str(tmp_path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_main_returns_1_on_dirty_path(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "dirty.tsx").write_text('<div className="bg-black" />\n', encoding="utf-8")
    assert main([str(tmp_path)]) == 1
    assert "forbidden token" in capsys.readouterr().err


def test_repo_frontend_and_streamlit_are_clean(repo_root: Path) -> None:
    """The committed theme files must themselves be clean."""
    findings = lint([repo_root / "frontend", repo_root / "streamlit_app"])
    assert findings == [], "\n".join(f.format() for f in findings)


def test_finding_format_contains_location() -> None:
    f = Finding(path=Path("a/b.tsx"), line_no=42, line="bad", rule="r")
    out = f.format()
    assert "a" in out and "b.tsx" in out and "42" in out and "r" in out


def test_forbidden_rules_compile() -> None:
    for pattern, _msg in FORBIDDEN_RULES:
        re.compile(pattern)
