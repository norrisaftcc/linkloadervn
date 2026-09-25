"""Load `story/assets.toml`.

Format:

    [bg]
    desert_night = "renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/images/bg desert night.png"

    [sprite.slim]
    neutral = "renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/images/slim neutral.png"
    talk = "renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/images/slim talk.png"

`[bg]` maps a `bg` statement's name to an image file. `[sprite.<id>]`
maps a `show`'s expression name, for that sprite id, to an image file.
Paths are relative to the repository root and are not moved or
copied — this file only points at art that already exists under
`renpy/`.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def load_assets(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"assets file not found: {path}")
    with open(path, "rb") as f:
        data = tomllib.load(f)
    data.setdefault("bg", {})
    data.setdefault("sprite", {})
    _check_shape(data, path)
    return data


def _check_shape(data: dict, path: Path) -> None:
    """Every mapped value must be a path string, and [sprite] must hold
    one table per sprite id. A ValueError here is reported by the CLI and
    the build as one error line, not a traceback."""
    if not isinstance(data["bg"], dict):
        raise ValueError(f"{path}: [bg] must be a table")
    for name, value in data["bg"].items():
        if not isinstance(value, str):
            raise ValueError(f"{path}: bg.{name} must be a path string, not {type(value).__name__}")
    if not isinstance(data["sprite"], dict):
        raise ValueError(f"{path}: [sprite] must hold one table per sprite")
    for sprite_id, table in data["sprite"].items():
        if not isinstance(table, dict):
            raise ValueError(f"{path}: sprite.{sprite_id} must be a table of expression = path")
        for expr, value in table.items():
            if not isinstance(value, str):
                raise ValueError(
                    f"{path}: sprite.{sprite_id}.{expr} must be a path string, not {type(value).__name__}"
                )
