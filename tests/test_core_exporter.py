"""Exporter tests: the JSON schema documented in
docs/scene-format.md round-trips a story's structure."""

from __future__ import annotations

import json

from linkloader.exporter import export_story
from linkloader.loader import load_cast_and_assets, load_story


def test_export_matches_documented_schema(demo_story_dir):
    story = load_story(demo_story_dir)
    cast, assets = load_cast_and_assets(demo_story_dir)
    data = export_story(story, cast, assets)

    assert set(data.keys()) == {"start", "scenes", "cast", "assets"}
    assert data["start"] == "start"
    assert set(data["scenes"].keys()) == set(story.scenes.keys())
    assert data["cast"]["slim"]["name"] == "Slim"
    assert "desert_night" in data["assets"]["bg"]

    # Every scene's statements list is JSON-serializable as-is.
    serialized = json.dumps(data)
    reloaded = json.loads(serialized)
    assert reloaded == data


def test_export_choice_condition_is_null_when_absent(make_story):
    story_dir = make_story(
        '== start\nchoice\n    "Go" -> start\n'
    )
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    data = export_story(story, cast, assets)
    choice = data["scenes"]["start"]["statements"][0]
    assert choice["kind"] == "choice"
    assert choice["options"][0]["condition"] is None


def test_export_check_outcomes_use_null_not_missing_keys(make_story):
    story_dir = make_story(
        "== start\ncheck coder vs 2\n    success -> start\n"
    )
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    data = export_story(story, cast, assets)
    check = data["scenes"]["start"]["statements"][0]
    assert check["outcomes"] == {
        "style": None,
        "success": "start",
        "tie": None,
        "fail": None,
    }


def test_export_nested_if_statements(make_story):
    story_dir = make_story(
        "== start\nif trust\n    > yes\nelse\n    > no\n"
    )
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    data = export_story(story, cast, assets)
    if_stmt = data["scenes"]["start"]["statements"][0]
    assert if_stmt["kind"] == "if"
    assert if_stmt["condition"] == {"flag": "trust", "op": "truthy", "value": None}
    assert if_stmt["then"] == [{"kind": "narration", "text": "yes"}]
    assert if_stmt["else"] == [{"kind": "narration", "text": "no"}]
