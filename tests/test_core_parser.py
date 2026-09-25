"""Parser tests: grammar acceptance and every parse error kind."""

from __future__ import annotations

import pytest

from linkloader.errors import ParseError
from linkloader.model import Bg, ChoiceStmt, IfStmt, Line, PuzzleStmt, Show
from linkloader.parser import parse_file


def _write(tmp_path, text):
    path = tmp_path / "s.scene"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_parses_every_statement_kind(tmp_path):
    text = """\
== start
bg desert_night
show slim neutral left
hide slim
slim: Hello there.
> Narration line.
set trust += 1, met_clipi = true
if trust >= 1
    slim: Trust is up.
else
    slim: Trust is down.
choice
    "Go." -> next
    "Stay." -> start [if met_clipi]
check coder vs 2
    style -> next
    success -> next
    tie -> next
    fail -> start
puzzle count-crew
    pass -> next
    lockout -> start

== next
-> start
"""
    scenes = parse_file(_write(tmp_path, text))
    assert [s.label for s in scenes] == ["start", "next"]
    start = scenes[0]
    kinds = [type(s).__name__ for s in start.statements]
    assert kinds == [
        "Bg",
        "Show",
        "Hide",
        "Line",
        "Narration",
        "SetStmt",
        "IfStmt",
        "ChoiceStmt",
        "CheckStmt",
        "PuzzleStmt",
    ]
    assert isinstance(start.statements[0], Bg) and start.statements[0].name == "desert_night"
    show = start.statements[1]
    assert isinstance(show, Show)
    assert (show.sprite, show.expression, show.position) == ("slim", "neutral", "left")


def test_show_defaults_position_to_center(tmp_path):
    text = '== start\nshow slim neutral\n> ok\n'
    scenes = parse_file(_write(tmp_path, text))
    show = scenes[0].statements[0]
    assert show.position == "center"


def test_bad_indent_raises_with_position(tmp_path):
    text = "== start\n> ok\n    > over-indented\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    err = exc.value
    assert err.code == "BadIndent"
    assert err.line == 3
    assert "s.scene" in err.file


def test_unrecognized_statement(tmp_path):
    text = "== start\nthis is not a statement\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "UnknownStatement"


def test_empty_choice_is_an_error(tmp_path):
    text = "== start\nchoice\n> nope\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "EmptyChoice"


def test_unreachable_choice_all_guarded(tmp_path):
    text = '== start\nchoice\n    "A" -> start [if never_true]\n'
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "UnreachableChoice"


def test_puzzle_needs_pass_outcome(tmp_path):
    text = "== start\npuzzle count-crew\n    lockout -> start\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "MissingPassOutcome"


def test_check_needs_at_least_one_outcome(tmp_path):
    text = "== start\ncheck coder vs 2\n> after\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "EmptyCheck"


def test_check_rejects_unknown_stat(tmp_path):
    text = "== start\ncheck luck vs 2\n    success -> start\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "UnknownStat"


def test_check_allows_partial_outcomes_for_fallthrough(tmp_path):
    # Only `success` given; `style`/`tie`/`fail` should fall through to
    # the next statement rather than being required.
    text = "== start\ncheck coder vs 2\n    success -> start\n> after\n"
    scenes = parse_file(_write(tmp_path, text))
    check = scenes[0].statements[0]
    assert check.outcomes == {"style": None, "success": "start", "tie": None, "fail": None}


def test_set_rejects_non_integer_increment(tmp_path):
    text = "== start\nset trust += true\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "BadValue"


def test_bad_condition(tmp_path):
    text = "== start\nif ???\n    > x\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "BadCondition"


def test_expected_scene_header_at_top(tmp_path):
    text = "not a header\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "ExpectedSceneHeader"


def test_tabs_are_rejected(tmp_path):
    text = "== start\n\t> x\n"
    with pytest.raises(ParseError) as exc:
        parse_file(_write(tmp_path, text))
    assert exc.value.code == "BadIndent"


def test_comments_and_blank_lines_are_ignored(tmp_path):
    text = "# a comment\n\n== start\n# another\n> ok\n\n"
    scenes = parse_file(_write(tmp_path, text))
    assert len(scenes) == 1
    assert len(scenes[0].statements) == 1
