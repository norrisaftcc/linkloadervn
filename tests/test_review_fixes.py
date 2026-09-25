"""Regression tests for the Copilot review of PR #1."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from linkloader.errors import ParseError
from linkloader.parser import parse_file

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "puzzles" / "check" / "run.sh"


def _scene(tmp_path, text):
    path = tmp_path / "s.scene"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_negative_difficulty_is_rejected(tmp_path):
    path = _scene(tmp_path, "== start\ncheck coder vs -1\n    success -> start\n")
    with pytest.raises(ParseError):
        parse_file(path)


@pytest.mark.parametrize("op", [">=", "<=", ">", "<"])
def test_ordering_against_a_boolean_is_rejected(tmp_path, op):
    path = _scene(tmp_path, f"== start\nif trust {op} true\n    > x\n")
    with pytest.raises(ParseError):
        parse_file(path)


def test_equality_against_a_boolean_is_allowed(tmp_path):
    path = _scene(tmp_path, "== start\nif met_clipi == true\n    > x\n")
    parse_file(path)


GOOD = "(stake haan-count (rig (roster) (reckon (husk? roster) 0 (sum 1 (haan-count (tull roster))))))\n"


@pytest.mark.parametrize(
    "source",
    [
        "(define (haan-count r) (length r))\n",
        "(stake haan-count (lambda (r) 0))\n",
        "(stake haan-count (rig (roster) (let ((n 0)) n)))\n",
        "(stake haan-count (rig (roster) 0 1))\n",
        "(stake haan-count (rig (roster) (reckon roster 1)))\n",
        GOOD + '(haan-count (seal (a "b")))\n',
    ],
)
def test_harness_rejects_forms_outside_rill(tmp_path, source):
    answer = tmp_path / "a.rill"
    answer.write_text(source, encoding="utf-8")
    result = subprocess.run(["bash", str(RUN), "count-crew", str(answer)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "not Rill" in result.stdout


def test_harness_accepts_pure_rill(tmp_path):
    answer = tmp_path / "a.rill"
    answer.write_text(GOOD, encoding="utf-8")
    result = subprocess.run(["bash", str(RUN), "count-crew", str(answer)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def _run_cli(args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "linkloader", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def _story_dir_missing_cast(tmp_path):
    story_dir = tmp_path / "story"
    story_dir.mkdir()
    (story_dir / "s.scene").write_text("== start\n> hi\n", encoding="utf-8")
    (story_dir / "assets.toml").write_text("", encoding="utf-8")
    return story_dir


def test_cli_reports_missing_cast_toml_as_an_error_not_a_traceback(tmp_path):
    story_dir = _story_dir_missing_cast(tmp_path)
    result = _run_cli(["check", str(story_dir)], cwd=ROOT)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "error:" in result.stderr
    assert "cast.toml" in result.stderr or "cast file not found" in result.stderr


def test_cli_reports_malformed_cast_toml_as_an_error_not_a_traceback(tmp_path):
    story_dir = _story_dir_missing_cast(tmp_path)
    (story_dir / "cast.toml").write_text("this is not [valid toml", encoding="utf-8")
    result = _run_cli(["check", str(story_dir)], cwd=ROOT)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "error:" in result.stderr


def test_cli_reports_cast_entry_missing_name_as_an_error_not_a_traceback(tmp_path):
    story_dir = _story_dir_missing_cast(tmp_path)
    (story_dir / "cast.toml").write_text("[slim]\nnotname = 1\n", encoding="utf-8")
    result = _run_cli(["check", str(story_dir)], cwd=ROOT)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "error:" in result.stderr


def test_check_missing_an_outcome_at_scene_end_is_flagged(tmp_path):
    from linkloader.loader import load_story
    from linkloader.validator import validate

    (tmp_path / "s.scene").write_text(
        "== start\ncheck coder vs 2\n    success -> start\n    fail -> start\n", encoding="utf-8"
    )
    story = load_story(tmp_path)
    _errors, warnings = validate(story, {}, {}, tmp_path)
    codes = [w.code for w in warnings]
    assert "OutcomeEndsGame" in codes


def test_unrelated_value_error_is_not_swallowed(monkeypatch):
    from linkloader import cli

    def boom(args):
        raise ValueError("a real bug")

    parser = cli.build_parser()
    monkeypatch.setattr(cli, "build_parser", lambda: parser)
    for action in parser._subparsers._group_actions[0].choices.values():
        action.set_defaults(func=boom)
    with pytest.raises(ValueError):
        cli.main(["check", "story/"])
