"""Load a whole story directory: every `.scene` file, plus cast.toml
and assets.toml alongside them.
"""

from __future__ import annotations

from pathlib import Path

from .assets import load_assets
from .cast import load_cast
from .errors import ValidationError
from .model import Story
from .parser import parse_file


def load_story(story_dir: Path) -> Story:
    story_dir = Path(story_dir)
    scenes: dict = {}
    files = sorted(p for p in story_dir.glob("*.scene"))
    for path in files:
        for scene in parse_file(str(path)):
            if scene.label in scenes:
                other = scenes[scene.label]
                raise ValidationError(
                    "DuplicateLabel",
                    f"scene {scene.label!r} defined twice: "
                    f"{other.pos} and {scene.pos}",
                )
            scenes[scene.label] = scene
    return Story(scenes=scenes, start="start", files=[str(p) for p in files])


def load_cast_and_assets(story_dir: Path) -> tuple[dict, dict]:
    story_dir = Path(story_dir)
    cast = load_cast(story_dir / "cast.toml")
    assets = load_assets(story_dir / "assets.toml")
    return cast, assets
