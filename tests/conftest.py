"""Shared pytest fixtures and config.

Phase 0 holds only the most basic fixtures. Each later phase adds its
own (e.g. tmp model checkpoints, fixture image batches) under the
relevant ``tests/<layer>/`` subdirectory.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Absolute path to the repository root.

    Resolves from this file's location so it is independent of the
    invocation cwd. Used by tests that need to read ``pyproject.toml``,
    ``frontend/``, ``streamlit_app/`` and similar repo-relative paths.
    """
    return Path(__file__).resolve().parent.parent
