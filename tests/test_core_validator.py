"""Validator tests: bad jumps, unreachable scenes, missing assets or
speakers, and the missing-puzzle-dir warning."""

from __future__ import annotations

from pathlib import Path

import pytest

from linkloader.errors import ValidationError
from linkloader.loader import load_cast_and_assets, load_story
from linkloader.validator import validate


def _validate(story_dir: Path, puzzles_dir: Path | None = None):
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    return validate(story, cast, assets, puzzles_dir or (story_dir.parent / "puzzles"))


def test_valid_demo_story_has_no_errors(demo_story_dir):
    errors, warnings = _validate(demo_story_dir, demo_story_dir.parent / "puzzles")
    assert errors == []


def test_bad_jump_target(make_story):
    story_dir = make_story(
        "== start\n> hi\n-> nowhere\n"
    )
    errors, warnings = _validate(story_dir)
    codes = [e.code for e in errors]
    assert "BadJump" in codes


def test_unreachable_scene(make_story):
    story_dir = make_story(
        "== start\n> hi\n\n== orphan\n> never reached\n"
    )
    errors, warnings = _validate(story_dir)
    codes = {e.code for e in errors}
    assert "UnreachableScene" in codes
    unreachable = [e for e in errors if e.code == "UnreachableScene"]
    assert unreachable[0].scene == "orphan"


def test_missing_start_scene(make_story):
    story_dir = make_story("== not_start\n> hi\n")
    errors, warnings = _validate(story_dir)
    assert any(e.code == "MissingStart" for e in errors)


def test_unknown_bg_asset(make_story):
    story_dir = make_story("== start\nbg nonexistent_bg\n")
    errors, warnings = _validate(story_dir)
    assert any(e.code == "UnknownAsset" for e in errors)


def test_unknown_speaker_in_dialogue(make_story):
    story_dir = make_story("== start\nnobody: hello\n")
    errors, warnings = _validate(story_dir)
    assert any(e.code == "UnknownSpeaker" for e in errors)


def test_unknown_sprite_expression(make_story):
    story_dir = make_story("== start\nshow slim smug\n")
    errors, warnings = _validate(story_dir)
    assert any(e.code == "UnknownAsset" for e in errors)


def test_missing_puzzle_dir_is_a_warning_not_an_error(make_story, tmp_path):
    story_dir = make_story(
        "== start\npuzzle no-such-puzzle\n    pass -> start\n"
    )
    empty_puzzles_dir = tmp_path / "no_puzzles_here"
    errors, warnings = _validate(story_dir, empty_puzzles_dir)
    assert errors == []
    assert any(w.code == "MissingPuzzleDir" for w in warnings)


def test_jump_inside_if_branch_is_checked(make_story):
    story_dir = make_story(
        "== start\nif trust\n    -> nowhere\nelse\n    > ok\n"
    )
    errors, warnings = _validate(story_dir)
    assert any(e.code == "BadJump" for e in errors)


def test_duplicate_label_across_the_same_file_is_rejected(make_story):
    story_dir = make_story("== start\n> a\n\n== start\n> b\n")
    with pytest.raises(ValidationError) as exc:
        load_story(story_dir)
    assert exc.value.code == "DuplicateLabel"
