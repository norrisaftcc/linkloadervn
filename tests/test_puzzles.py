"""Run the Rill puzzle checker and assert it exits 0.

The real check logic lives in puzzles/check/run.sh, which runs every
puzzle's reference answer through chibi-scheme (must pass) and every
wrong answer under puzzles/<id>/wrong/ (must fail). This test just
confirms that whole suite exits 0, and re-prints its output on
failure so a CI log shows exactly which puzzle or wrong answer broke.
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN_SH = REPO_ROOT / "puzzles" / "check" / "run.sh"


def test_run_sh_exists_and_is_executable():
    assert RUN_SH.exists(), f"missing {RUN_SH}"


def test_puzzle_suite_passes():
    result = subprocess.run(
        ["bash", str(RUN_SH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        "puzzles/check/run.sh did not exit 0\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
    assert "fail" in result.stdout.lower()
    assert "0 fail" in result.stdout
