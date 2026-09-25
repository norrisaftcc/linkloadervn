"""Tests for the `mode` statement: parsing, `UnknownMode` validation,
the export shape, and that the terminal player ignores it.

See docs/scene-format.md, "`mode` — the runner's visual mode"."""

from __future__ import annotations

from pathlib import Path

from linkloader.loader import load_cast_and_assets, load_story
from linkloader.model import ModeStmt
from linkloader.parser import parse_file
from linkloader.player import Player
from linkloader.validator import validate


def _write(tmp_path, text):
    path = tmp_path / "s.scene"
    path.write_text(text, encoding="utf-8")
    return str(path)


# -- parser -------------------------------------------------------------


def test_parses_mode_statement(tmp_path):
    scenes = parse_file(_write(tmp_path, "== start\nmode inner\n> hi\n"))
    stmt = scenes[0].statements[0]
    assert isinstance(stmt, ModeStmt)
    assert stmt.name == "inner"


def test_parses_mode_default(tmp_path):
    scenes = parse_file(_write(tmp_path, "== start\nmode default\n"))
    assert scenes[0].statements[0].name == "default"


def test_parser_accepts_any_identifier_as_a_mode_name(tmp_path):
    """The parser accepts any identifier here, the same way it does
    for `bg`; only the validator knows which names are real."""
    scenes = parse_file(_write(tmp_path, "== start\nmode sideways\n"))
    assert scenes[0].statements[0].name == "sideways"


def test_mode_is_allowed_inside_an_if_block(tmp_path):
    scenes = parse_file(
        _write(tmp_path, "== start\nif trust\n    mode inner\n")
    )
    if_stmt = scenes[0].statements[0]
    assert isinstance(if_stmt.then[0], ModeStmt)
    assert if_stmt.then[0].name == "inner"


# -- validator ------------------------------------------------------------


def test_unknown_mode_is_a_validation_error(make_story):
    story_dir = make_story("== start\nmode sideways\n")
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    errors, warnings = validate(story, cast, assets, story_dir.parent / "puzzles")
    codes = [e.code for e in errors]
    assert "UnknownMode" in codes
    bad = next(e for e in errors if e.code == "UnknownMode")
    assert bad.scene == "start"


def test_known_modes_pass_validation(make_story):
    story_dir = make_story("== start\nmode default\nmode inner\n")
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    errors, warnings = validate(story, cast, assets, story_dir.parent / "puzzles")
    assert [e.code for e in errors if e.code == "UnknownMode"] == []


# -- exporter ---------------------------------------------------------------


def test_export_shape_is_exactly_kind_and_name(make_story):
    from linkloader.exporter import export_story

    story_dir = make_story("== start\nmode inner\n")
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    data = export_story(story, cast, assets)
    stmt = data["scenes"]["start"]["statements"][0]
    assert stmt == {"kind": "mode", "name": "inner"}


# -- terminal player --------------------------------------------------------


def test_player_ignores_mode(make_story, repo_root: Path):
    story_dir = make_story(
        "== start\nmode inner\n> after the mode line\n-> ending\n\n== ending\n> the end\n"
    )
    story = load_story(story_dir)
    cast, assets = load_cast_and_assets(story_dir)
    errors, warnings = validate(story, cast, assets, repo_root / "puzzles")
    assert errors == [], errors

    output: list[str] = []
    player = Player(story, cast, root=repo_root, seed=0, script=[], out=output.append)
    ending = player.run()

    assert ending == "ending"
    # The player prints a bracketed notice for every other statement it
    # handles (e.g. "[bg: ...]"); `mode` gets none at all.
    assert not any(line.startswith("[mode") for line in output)
    assert output == ["\n== start ==", "> after the mode line", "\n== ending ==", "> the end"]
