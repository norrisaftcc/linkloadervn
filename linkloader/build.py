"""`python -m linkloader build story/ -o dist/`

Builds the one-folder static web game:

- `dist/story.json` — the exporter's scene JSON, extended with
  "ladder", "puzzles", and "lexicon" per contract C2 (see
  docs/scene-format.md and exporter.py).
- `dist/index.html`, `dist/runner.js`, `dist/stage.css` (and any other
  file living directly under `web/`) — copied from the web runner.
- `dist/rill/` — copied from `web/rill/` (the Rill evaluator; a
  separate part of the project).
- `dist/tokens.css` — copied from `docs/style/tokens.css`.
- `dist/assets/` — only the background and sprite images the story
  actually references, flattened to safe filenames.

Nothing here edits `web/`, `web/rill/`, `docs/`, or `story/`; it only
reads them. Source of truth stays the scene files and puzzles/ (see
AGENTS.md).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from .exporter import build_ladder, build_lexicon, build_puzzles_data, export_story
from .loader import load_cast_and_assets, load_story
from .model import Bg, PuzzleStmt, Show, Story
from .validator import validate, walk_statements

# web/ lives next to linkloader/ at the repo root.
DEFAULT_WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class BuildError(RuntimeError):
    """The build was refused: the story failed validation, or an asset
    the story references is missing on disk."""


def referenced_assets(story: Story, assets: dict) -> dict:
    """The subset of `assets` (the loaded assets.toml dict) that the
    story's statements actually use, in the same {"bg": {...},
    "sprite": {...}} shape."""
    used_bg: set[str] = set()
    used_sprite_expr: set[tuple[str, str]] = set()
    for scene in story.scenes.values():
        for stmt in walk_statements(scene.statements):
            if isinstance(stmt, Bg):
                used_bg.add(stmt.name)
            elif isinstance(stmt, Show):
                used_sprite_expr.add((stmt.sprite, stmt.expression))

    bg_assets = assets.get("bg", {})
    sprite_assets = assets.get("sprite", {})

    bg = {name: bg_assets[name] for name in used_bg if name in bg_assets}
    sprite: dict = {}
    for sprite_id, expr in used_sprite_expr:
        path = sprite_assets.get(sprite_id, {}).get(expr)
        if path is not None:
            sprite.setdefault(sprite_id, {})[expr] = path
    return {"bg": bg, "sprite": sprite}


def referenced_puzzle_ids(story: Story) -> list[str]:
    ids: set[str] = set()
    for scene in story.scenes.values():
        for stmt in walk_statements(scene.statements):
            if isinstance(stmt, PuzzleStmt):
                ids.add(stmt.puzzle_id)
    return sorted(ids)


def _dist_asset_name(original_rel_path: str) -> str:
    """A flat, web-safe filename for a copied asset. Repo asset
    filenames contain spaces (see story/assets.toml); browsers are
    fine with that in a path, but we normalize anyway so URLs in
    story.json need no percent-escaping."""
    return Path(original_rel_path).name.replace(" ", "_")


def _copy_assets(used_assets: dict, root: Path, dist_assets_dir: Path) -> dict:
    """Copies each referenced asset into `dist_assets_dir`. Returns the
    same {"bg": ..., "sprite": ...} shape, rewritten to
    "assets/<file>" paths relative to dist/index.html."""
    dist_assets_dir.mkdir(parents=True, exist_ok=True)
    out: dict = {"bg": {}, "sprite": {}}

    def copy_one(rel_path: str) -> str:
        src = root / rel_path
        if not src.exists():
            raise BuildError(f"asset referenced by the story is missing on disk: {src}")
        dist_name = _dist_asset_name(rel_path)
        shutil.copyfile(src, dist_assets_dir / dist_name)
        return f"assets/{dist_name}"

    for name, rel_path in used_assets["bg"].items():
        out["bg"][name] = copy_one(rel_path)
    for sprite_id, exprs in used_assets["sprite"].items():
        out["sprite"][sprite_id] = {expr: copy_one(path) for expr, path in exprs.items()}
    return out


def _copy_web_runner(dist_dir: Path, web_dir: Path) -> None:
    """Copies every file directly under web/ (index.html, runner.js,
    stage.css, ...) except the web/rill/ subtree, then copies
    web/rill/ into dist/rill/ verbatim."""
    if not web_dir.is_dir():
        raise BuildError(f"web runner directory not found: {web_dir}")
    for item in sorted(web_dir.iterdir()):
        if item.name == "rill":
            continue
        if item.is_file():
            shutil.copyfile(item, dist_dir / item.name)

    rill_src = web_dir / "rill"
    rill_dst = dist_dir / "rill"
    rill_dst.mkdir(parents=True, exist_ok=True)
    if rill_src.is_dir():
        for item in sorted(rill_src.iterdir()):
            # Ship the evaluator itself, not its own test file(s).
            if item.is_file() and ".test." not in item.name:
                shutil.copyfile(item, rill_dst / item.name)


def build(
    story_dir: Path,
    out_dir: Path,
    root: Path,
    web_dir: Path | None = None,
) -> dict:
    """Runs the whole build. Returns a small report dict:
    {"scenes": int, "warnings": [str, ...], "puzzle_ids": [str, ...],
    "assets_copied": int}. Raises BuildError (validation failed, a
    referenced asset is missing) or LinkLoaderError (bad story/cast/
    assets files) rather than writing a partial dist/."""
    story_dir = Path(story_dir)
    out_dir = Path(out_dir)
    root = Path(root)
    web_dir = web_dir or DEFAULT_WEB_DIR

    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    puzzles_dir = root / "puzzles"
    errors, warnings = validate(story, cast, assets, puzzles_dir)
    if errors:
        raise BuildError(
            "story failed validation; build refused:\n"
            + "\n".join(f"  {e}" for e in errors)
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    data = export_story(story, cast, assets)
    used_assets = referenced_assets(story, assets)
    data["assets"] = _copy_assets(used_assets, root, out_dir / "assets")
    data["ladder"] = build_ladder()
    puzzle_ids = referenced_puzzle_ids(story)
    data["puzzles"] = build_puzzles_data(puzzles_dir, puzzle_ids)
    lexicon_path = puzzles_dir / "rill" / "lexicon.md"
    data["lexicon"] = (
        build_lexicon(lexicon_path.read_text(encoding="utf-8")) if lexicon_path.exists() else []
    )

    (out_dir / "story.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    tokens_src = root / "docs" / "style" / "tokens.css"
    if tokens_src.exists():
        shutil.copyfile(tokens_src, out_dir / "tokens.css")

    _copy_web_runner(out_dir, web_dir)

    assets_copied = len(data["assets"]["bg"]) + sum(
        len(v) for v in data["assets"]["sprite"].values()
    )
    return {
        "scenes": len(story.scenes),
        "warnings": [str(w) for w in warnings],
        "puzzle_ids": puzzle_ids,
        "assets_copied": assets_copied,
    }
