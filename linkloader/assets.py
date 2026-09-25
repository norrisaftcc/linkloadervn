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
    return data
