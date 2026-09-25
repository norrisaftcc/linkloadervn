"""Run the JS Rill test suite (web/rill/) under Node's test runner.

The real tests live in web/rill/rill.test.mjs, which parity-checks
web/rill/rill.js against puzzles/cases.json and against chibi-scheme
itself (via puzzles/check/run.sh). This confirms `node --test` over
web/rill/ exits 0, and re-prints its output on failure.

Note: `node --test web/rill/` (a bare directory argument) does not
recurse on the Node build in this environment (v22.22.2) -- it tries
to `require()` the directory itself and fails with MODULE_NOT_FOUND,
even though Node's docs say a directory argument should be walked for
test files. Confirmed as a general Node quirk here, not specific to
this repo, with a minimal reproduction outside it. Passing the
*.test.mjs files explicitly (as node --test's own multi-file form)
works around it and exercises the same suite.
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RILL_JS_DIR = REPO_ROOT / "web" / "rill"


def test_rill_js_exists():
    assert (RILL_JS_DIR / "rill.js").exists(), "missing web/rill/rill.js"
    assert (RILL_JS_DIR / "rill.test.mjs").exists(), "missing web/rill/rill.test.mjs"


def test_node_test_suite_passes():
    test_files = sorted(str(p) for p in RILL_JS_DIR.glob("*.test.mjs"))
    assert test_files, "no *.test.mjs files found under web/rill/"

    result = subprocess.run(
        ["node", "--test", *test_files],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        "node --test web/rill/ did not exit 0\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
