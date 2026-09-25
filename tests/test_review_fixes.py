"""Regression tests for the Copilot review of PR #1."""

from __future__ import annotations

import subprocess
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
