"""Exporter tests: the JSON schema documented in
docs/scene-format.md round-trips a story's structure."""

from __future__ import annotations

import json

from linkloader.exporter import build_lexicon, export_story
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


# -- build_lexicon (puzzles/rill/lexicon.md -> story.json "lexicon") ------


def test_build_lexicon_parses_the_real_lexicon(repo_root):
    text = (repo_root / "puzzles" / "rill" / "lexicon.md").read_text(encoding="utf-8")
    entries = build_lexicon(text)

    grammar = [e for e in entries if e["kind"] == "grammar"]
    theme = [e for e in entries if e["kind"] == "theme"]
    assert len(grammar) == 12
    assert len(theme) == 8

    by_word = {e["word"]: e for e in entries}
    assert by_word["husk?"] == {
        "word": "husk?",
        "gloss": "is the hold empty, a husk?",
        "kind": "grammar",
        "scheme": "null?",
    }
    assert by_word["fen"] == {
        "word": "fen",
        "gloss": "home, harbor",
        "kind": "theme",
        "scheme": None,
    }


def test_build_lexicon_is_robust_to_formatting_noise():
    text = """# Rill

## Grammar roots (2)

Some intro prose that isn't a table row.

| Rill     | Scheme    | Gloss                |
|----------|-----------|----------------------|
| `stake`   |`define`|  to stake a claim — name it   |
|`rig`|`lambda`|to rig|

## Thematic roots (2)

|Rill|Gloss|
|---|---|
| `drev` | star |
|`fen`|home, harbor|

## Why the mapping holds

Some closing prose, not a table.
"""
    entries = build_lexicon(text)
    assert entries == [
        {"word": "stake", "gloss": "to stake a claim — name it", "kind": "grammar", "scheme": "define"},
        {"word": "rig", "gloss": "to rig", "kind": "grammar", "scheme": "lambda"},
        {"word": "drev", "gloss": "star", "kind": "theme", "scheme": None},
        {"word": "fen", "gloss": "home, harbor", "kind": "theme", "scheme": None},
    ]


def test_build_lexicon_ignores_unrelated_headings_and_empty_text():
    text = "## Some other section\n\n| a | b |\n|---|---|\n| x | y |\n"
    assert build_lexicon(text) == []
    assert build_lexicon("") == []
