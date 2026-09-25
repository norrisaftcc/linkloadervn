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


def test_reroll_spends_a_fate_point(demo_story_dir, repo_root):
    story, cast, _assets = _load(demo_story_dir, repo_root)
    answer = str(repo_root / "puzzles" / "count-crew" / "answer.rill")
    script = ["1", "y", answer]
    player = Player(
        story, cast, root=repo_root, seed=0, script=script, fate_points=3, out=lambda *_: None
    )
    player.run()
    assert player.fate == 2
