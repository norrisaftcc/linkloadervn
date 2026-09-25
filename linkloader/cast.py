"""Load `story/cast.toml`.

Format:

    [slim]
    name = "Slim"

    [terminal]
    name = "Terminal"

Every top-level table key is a speaker id, usable as a dialogue
speaker or a `show`/`hide` sprite name. `name` is the display name a
player-facing tool should print; nothing else is required.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def load_cast(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"cast file not found: {path}")
    with open(path, "rb") as f:
        data = tomllib.load(f)
    for speaker_id, entry in data.items():
        if not isinstance(entry, dict) or "name" not in entry:
            raise ValueError(f"{path}: cast entry {speaker_id!r} needs a `name` field")
    return data
