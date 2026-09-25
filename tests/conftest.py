"""Shared fixtures for linkloader's core test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo_root() -> Path:
    """The real repository root, where puzzles/ and story/ live."""
    return REPO_ROOT


@pytest.fixture
def demo_story_dir(repo_root: Path) -> Path:
    """The demo story fixture (demo.scene, cast.toml, assets.toml):
    a small story exercising every statement in the format, used by
    the core test suite. Moved out of story/ so that directory holds
    only the real story (see tests/test_story.py)."""
    return repo_root / "tests" / "fixtures" / "demo"


@pytest.fixture
def make_story(tmp_path: Path):
    """Write a minimal, self-contained story directory under tmp_path.

    `make_story(scene_text, cast=None, assets=None)` writes
    `demo.scene` plus a small default cast.toml/assets.toml (or the
    caller's own), and returns the story directory path. Kept small on
    purpose: most tests only care about one or two statements.
    """

    default_cast = """
[slim]
name = "Slim"

[terminal]
name = "Terminal"
"""
    default_assets = """
[bg]
desert_night = "images/bg desert night.png"

[sprite.slim]
neutral = "images/slim neutral.png"
"""

    def _make(scene_text: str, cast: str | None = None, assets: str | None = None) -> Path:
        story_dir = tmp_path / "story"
        story_dir.mkdir(exist_ok=True)
        (story_dir / "demo.scene").write_text(scene_text, encoding="utf-8")
        (story_dir / "cast.toml").write_text(cast or default_cast, encoding="utf-8")
        (story_dir / "assets.toml").write_text(assets or default_assets, encoding="utf-8")
        return story_dir

    return _make
