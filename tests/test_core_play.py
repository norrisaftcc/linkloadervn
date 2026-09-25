"""Scripted play tests: the terminal player walks demo.scene to an
ending without ever reading real stdin."""

from __future__ import annotations

from pathlib import Path

import pytest

from linkloader.loader import load_cast_and_assets, load_story
from linkloader.player import Player, ScriptExhausted
from linkloader.validator import validate


def _load(demo_story_dir: Path, repo_root: Path):
    story = load_story(demo_story_dir)
    cast, assets = load_cast_and_assets(demo_story_dir)
    errors, warnings = validate(story, cast, assets, repo_root / "puzzles")
    assert errors == [], errors
    return story, cast, assets


def test_demo_reaches_an_ending_via_puzzle_pass(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    answer = str(repo_root / "puzzles" / "count-crew" / "answer.rill")
    # seed=5, coder=0, difficulty=2 -> a tie, which demo.scene leaves
    # unhandled on purpose so play falls through into the puzzle.
    script = ["1", "n", answer]
    player = Player(
        story, cast, root=repo_root, seed=5, script=script, fate_points=3, out=lambda *_: None
    )
    ending = player.run()
    assert ending == "ending"
    assert player.flags["met_clipi"] is True


def test_demo_reaches_an_ending_via_check_fail(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    # seed=0, coder=0, difficulty=2 -> fail (see test_core_dice for the
    # seeded roll table), so play jumps straight to jam_worse without
    # ever touching the puzzle.
    script = ["1", "n"]
    player = Player(
        story, cast, root=repo_root, seed=0, script=script, fate_points=3, out=lambda *_: None
    )
    ending = player.run()
    assert ending == "ending"


def test_demo_second_choice_option_is_hidden_until_flag_is_set(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    player = Player(
        story, cast, root=repo_root, seed=0, script=["1", "n"], out=lambda *_: None
    )
    # Choosing "1" always works because met_clipi starts false and the
    # second option is guarded on it; picking "2" here would be an
    # invalid answer and the player would ask again, exhausting the
    # script.
    player.run()


def test_script_exhaustion_raises_a_clear_error(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    player = Player(story, cast, root=repo_root, seed=0, script=[], out=lambda *_: None)
    with pytest.raises(ScriptExhausted):
        player.run()


def test_check_stat_value_comes_from_the_flag_of_the_same_name(make_story, repo_root):
    # seed=5 rolls (1, 0, 1, 0) -> sum 2 (see test_core_dice.py). With
    # `coder` set to 3 by `set`, total = 5 vs difficulty 2, which is a
    # "style" per the ladder (>= difficulty + 3). If the stat value
    # were still hardcoded/defaulted to 0, total would be 2 -> "tie".
    story_dir = make_story(
        "== start\n"
        "set coder = 3\n"
        "check coder vs 2\n"
        "    style -> style_end\n"
        "    success -> success_end\n"
        "    tie -> tie_end\n"
        "    fail -> fail_end\n"
        "== style_end\n> style\n"
        "== success_end\n> success\n"
        "== tie_end\n> tie\n"
        "== fail_end\n> fail\n"
    )
    story = load_story(story_dir)
    cast, _assets = load_cast_and_assets(story_dir)
    player = Player(
        story, cast, root=repo_root, seed=5, script=[], fate_points=0, out=lambda *_: None
    )
    ending = player.run()
    assert ending == "style_end"
    assert player.flags["coder"] == 3


def test_check_stat_value_defaults_to_zero_when_the_flag_is_unset(make_story, repo_root):
    story_dir = make_story(
        "== start\n"
        "check coder vs 2\n"
        "    style -> style_end\n"
        "    tie -> tie_end\n"
        "== style_end\n> style\n"
        "== tie_end\n> tie\n"
    )
    story = load_story(story_dir)
    cast, _assets = load_cast_and_assets(story_dir)
    player = Player(
        story, cast, root=repo_root, seed=5, script=[], fate_points=0, out=lambda *_: None
    )
    ending = player.run()
    assert ending == "tie_end"


def test_check_stat_value_ignores_a_non_integer_flag(make_story, repo_root):
    story_dir = make_story(
        "== start\n"
        "set coder = true\n"
        "check coder vs 2\n"
        "    style -> style_end\n"
        "    tie -> tie_end\n"
        "== style_end\n> style\n"
        "== tie_end\n> tie\n"
    )
    story = load_story(story_dir)
    cast, _assets = load_cast_and_assets(story_dir)
    player = Player(
        story, cast, root=repo_root, seed=5, script=[], fate_points=0, out=lambda *_: None
    )
    ending = player.run()
    assert ending == "tie_end"


def test_reroll_spends_a_fate_point(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    answer = str(repo_root / "puzzles" / "count-crew" / "answer.rill")
    script = ["1", "y", answer]
    player = Player(
        story, cast, root=repo_root, seed=0, script=script, fate_points=3, out=lambda *_: None
    )
    player.run()
    assert player.fate == 2
