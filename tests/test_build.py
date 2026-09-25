"""Tests for `python -m linkloader build`: the static web game build
(linkloader/build.py). See docs/scene-format.md and the SHARED
CONTRACTS note in the web runner's own files for the story.json
shape this checks."""

from __future__ import annotations

import json

from linkloader.build import BuildError, build, referenced_assets, referenced_puzzle_ids
from linkloader.loader import load_cast_and_assets, load_story


def test_build_writes_required_files(repo_root, demo_story_dir, tmp_path):
    out_dir = tmp_path / "dist"
    report = build(demo_story_dir, out_dir, repo_root)

    for name in ("index.html", "runner.js", "stage.css", "story.json", "tokens.css"):
        assert (out_dir / name).exists(), f"missing dist/{name}"
    assert report["scenes"] > 0


def test_story_json_has_ladder_puzzles_start(repo_root, demo_story_dir, tmp_path):
    out_dir = tmp_path / "dist"
    build(demo_story_dir, out_dir, repo_root)
    data = json.loads((out_dir / "story.json").read_text(encoding="utf-8"))

    assert data["start"] == "start"

    assert "ladder" in data
    ladder = data["ladder"]
    assert ladder["faces"] == [-1, 0, 1]
    tier_names = {row["tier"] for row in ladder["tiers"]}
    assert tier_names == {"style", "success", "tie", "fail"}

    assert "puzzles" in data
    # The demo story only reaches count-crew (see story/demo.scene).
    assert "count-crew" in data["puzzles"]
    entry = data["puzzles"]["count-crew"]
    assert set(entry.keys()) == {"id", "title", "prompt", "starter", "hint", "cases"}
    assert entry["id"] == "count-crew"
    assert entry["starter"]  # non-empty: starter.rill exists for this puzzle
    assert isinstance(entry["cases"], list) and len(entry["cases"]) > 0


def test_every_referenced_asset_exists_in_dist(repo_root, demo_story_dir, tmp_path):
    out_dir = tmp_path / "dist"
    build(demo_story_dir, out_dir, repo_root)
    data = json.loads((out_dir / "story.json").read_text(encoding="utf-8"))

    assets = data["assets"]
    checked = 0
    for _name, rel_path in assets.get("bg", {}).items():
        assert (out_dir / rel_path).exists(), f"missing bg asset: {rel_path}"
        checked += 1
    for _sprite_id, exprs in assets.get("sprite", {}).items():
        for _expr, rel_path in exprs.items():
            assert (out_dir / rel_path).exists(), f"missing sprite asset: {rel_path}"
            checked += 1
    assert checked > 0


def test_referenced_assets_only_includes_what_the_story_uses(repo_root, demo_story_dir):
    story = load_story(demo_story_dir)
    _cast, assets = load_cast_and_assets(demo_story_dir)
    used = referenced_assets(story, assets)

    # story/demo.scene never shows clipi "smug" or "glitch", and never
    # shows terminal "talk" -- those must be left out.
    assert "smug" not in used["sprite"].get("clipi", {})
    assert "glitch" not in used["sprite"].get("clipi", {})
    assert "talk" not in used["sprite"].get("terminal", {})
    # But it does show clipi "talk", slim "neutral"/"laughing", and terminal "idle".
    assert used["sprite"]["clipi"] == {"talk": assets["sprite"]["clipi"]["talk"]}
    assert set(used["sprite"]["slim"]) == {"neutral", "laughing"}
    assert set(used["sprite"]["terminal"]) == {"idle"}
    assert "desert_night" in used["bg"]


def test_referenced_puzzle_ids(repo_root, demo_story_dir):
    story = load_story(demo_story_dir)
    assert referenced_puzzle_ids(story) == ["count-crew"]


def test_build_refuses_a_story_that_fails_validation(repo_root, make_story, tmp_path):
    # A jump to a label that does not exist is a BadJump validation error.
    story_dir = make_story("== start\n-> nowhere\n")
    out_dir = tmp_path / "dist"
    try:
        build(story_dir, out_dir, repo_root)
        assert False, "expected BuildError"
    except BuildError:
        pass
    assert not (out_dir / "story.json").exists()


def test_build_raises_on_missing_asset_file(repo_root, make_story, tmp_path):
    story_dir = make_story(
        "== start\nbg desert_night\n> hi\n",
        assets='\n[bg]\ndesert_night = "images/does_not_exist.png"\n\n[sprite.slim]\n',
    )
    out_dir = tmp_path / "dist"
    try:
        build(story_dir, out_dir, repo_root)
        assert False, "expected BuildError"
    except BuildError as e:
        assert "does_not_exist.png" in str(e)
