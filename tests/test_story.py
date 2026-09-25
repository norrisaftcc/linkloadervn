"""Tests for the real story in story/: `linkloader check` passes with
zero warnings, scripted plays reach every ending, and each puzzle's
pass and lockout paths are reachable.

None of the checks here in the linkloader story use a `check` outcome
to gate which scene comes next (every tier converges on the same
follow-on scene; see 02-sabotage.scene, 03-clipi.scene, and
04-confrontation.scene) - only puzzle pass/lockout and player choices
do. That means a fixed seed's dice rolls never change which ending a
script reaches, so every test below can share one seed and differ
only in which choices and puzzle answers the script feeds in.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from linkloader.loader import load_cast_and_assets, load_story
from linkloader.player import Player
from linkloader.validator import validate

STATS = {"cosmonaut": 1, "cowboy": 1, "coder": 1}
SEED = 1  # arbitrary and irrelevant to reachability; see module docstring.


@pytest.fixture
def story_dir(repo_root: Path) -> Path:
    return repo_root / "story"


def _load(story_dir: Path, repo_root: Path):
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    errors, warnings = validate(story, cast, assets, repo_root / "puzzles")
    assert errors == [], errors
    assert warnings == [], warnings
    return story, cast


def _play(story_dir: Path, repo_root: Path, script: list[str]):
    """Runs the real story with a scripted input queue. Returns
    (ending_label, flags, list_of_scene_labels_visited)."""
    story, cast = _load(story_dir, repo_root)
    visited: list[str] = []

    def _out(line: str) -> None:
        text = str(line)
        if text.startswith("\n== ") and text.endswith(" =="):
            visited.append(text.strip()[3:-3])

    player = Player(
        story,
        cast,
        root=repo_root,
        seed=SEED,
        script=list(script),
        fate_points=3,
        stats=STATS,
        out=_out,
    )
    ending = player.run()
    return ending, player.flags, visited


def _answer(repo_root: Path, puzzle_id: str) -> str:
    return str(repo_root / "puzzles" / puzzle_id / "answer.rill")


def _wrong(repo_root: Path, puzzle_id: str, name: str) -> str:
    return str(repo_root / "puzzles" / puzzle_id / "wrong" / name)


# -- `linkloader check story/` -------------------------------------------


def test_check_story_passes_with_zero_warnings(repo_root: Path, story_dir: Path):
    result = subprocess.run(
        [sys.executable, "-m", "linkloader", "check", str(story_dir)],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "warning:" not in result.stdout
    assert "warning:" not in result.stderr
    assert "0 warning(s)" in result.stdout


# -- endings ---------------------------------------------------------------


def test_reaches_ending_company(repo_root: Path, story_dir: Path):
    script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",  # cut the channel: no rustler sympathy
        "n",
        _answer(repo_root, "find-signal"),
        "1",  # report to the Company
    ]
    ending, flags, visited = _play(story_dir, repo_root, script)
    assert ending == "ending_company"
    assert flags.get("rustler_sympathy", 0) == 0
    assert "rustler_expelled" in visited


def test_reaches_ending_mercy(repo_root: Path, story_dir: Path):
    script = [
        "2",
        "2",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "2",  # let it go
    ]
    ending, flags, visited = _play(story_dir, repo_root, script)
    assert ending == "ending_mercy"


def test_reaches_ending_defect_after_asking_the_rustlers_why(repo_root: Path, story_dir: Path):
    script = [
        "3",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "1",  # ask them why -> rustler_sympathy
        "n",
        _answer(repo_root, "find-signal"),
        "3",  # copy what they were reaching for
    ]
    ending, flags, visited = _play(story_dir, repo_root, script)
    assert ending == "ending_defect"
    assert flags["rustler_sympathy"] >= 1


def test_resolution_hides_the_defect_option_without_rustler_sympathy(
    repo_root: Path, story_dir: Path
):
    """The `[if rustler_sympathy >= 1]` guard on the third resolution
    option actually hides it: only two options are offered when the
    player cut the rustlers off instead of asking why."""
    story, cast = _load(story_dir, repo_root)
    lines: list[str] = []
    script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",  # cut the channel
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    player = Player(
        story,
        cast,
        root=repo_root,
        seed=SEED,
        script=list(script),
        fate_points=3,
        stats=STATS,
        out=lines.append,
    )
    player.run()
    start = lines.index("\n== resolution ==")
    resolution_menu = "\n".join(lines[start:])
    assert "1. Report the relay point to the Company." in resolution_menu
    assert "2. Let it go. Say the trail went cold." in resolution_menu
    assert "3. Copy what they were reaching for" not in resolution_menu


def test_find_signal_lockout_reaches_ending_escaped(repo_root: Path, story_dir: Path):
    script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "1",
        "n",
        _wrong(repo_root, "find-signal", "wrong-base-case.rill"),
    ]
    ending, flags, visited = _play(story_dir, repo_root, script)
    assert ending == "ending_escaped"
    assert "rustler_escaped" in visited


# -- each puzzle's pass and lockout paths ----------------------------------


def test_decode_buoy_pass_and_lockout_both_reachable(repo_root: Path, story_dir: Path):
    pass_script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    _, _, visited_pass = _play(story_dir, repo_root, pass_script)
    assert "transmission_clear" in visited_pass
    assert "transmission_garbled" not in visited_pass

    lockout_script = [
        "1",
        "1",
        _wrong(repo_root, "decode-buoy", "wrong-word.rill"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    _, flags, visited_lockout = _play(story_dir, repo_root, lockout_script)
    assert "transmission_garbled" in visited_lockout
    assert flags["messy_fix"] is True


def test_count_crew_pass_and_lockout_both_reachable(repo_root: Path, story_dir: Path):
    pass_script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    _, flags_pass, visited_pass = _play(story_dir, repo_root, pass_script)
    assert "clipi_recovered" in visited_pass
    assert flags_pass["clipi_stable"] is True

    lockout_script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _wrong(repo_root, "count-crew", "wrong-base-case.rill"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    _, flags_lockout, visited_lockout = _play(story_dir, repo_root, lockout_script)
    assert "clipi_destabilized" in visited_lockout
    assert flags_lockout["clipi_stable"] is False


def test_find_signal_pass_and_lockout_both_reachable(repo_root: Path, story_dir: Path):
    pass_script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _answer(repo_root, "find-signal"),
        "1",
    ]
    ending_pass, _, visited_pass = _play(story_dir, repo_root, pass_script)
    assert "rustler_expelled" in visited_pass
    assert ending_pass == "ending_company"

    lockout_script = [
        "1",
        "1",
        _answer(repo_root, "decode-buoy"),
        "n",
        "n",
        _answer(repo_root, "count-crew"),
        "2",
        "n",
        _wrong(repo_root, "find-signal", "wrong-base-case.rill"),
    ]
    ending_lockout, _, visited_lockout = _play(story_dir, repo_root, lockout_script)
    assert "rustler_escaped" in visited_lockout
    assert ending_lockout == "ending_escaped"
