"""Test that ``medxai.__version__`` is exposed and matches ``pyproject.toml``."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import medxai


def test_version_is_exposed() -> None:
    assert isinstance(medxai.__version__, str)
    assert medxai.__version__, "medxai.__version__ must not be empty"


def test_version_matches_semver() -> None:
    # Permissive semver: MAJOR.MINOR.PATCH with optional pre-release / build.
    pattern = r"^\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?$"
    assert re.match(pattern, medxai.__version__) is not None, (
        f"medxai.__version__={medxai.__version__!r} is not semver-shaped"
    )


def test_version_matches_pyproject(repo_root: Path) -> None:
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == medxai.__version__, (
        "pyproject.toml [project].version drifted from src/medxai/__init__.py"
    )
