"""End-to-end test for the `mode` statement in the web runner.

Builds a tiny story (a copy of tests/fixtures/demo/ with one extra
scene using `mode inner`) into a temp dist/, serves it, and drives it
with Playwright to check that `#game`'s `data-mode` attribute becomes
"inner" in that scene and resets to "default" after a jump.

Skips cleanly (pytest.skip) if Playwright or the pinned Chromium build
is missing, the same way tests/e2e/test_web.py does.

See docs/plans/wave2.md section 5 items 2-3 and docs/scene-format.md,
"`mode` — the runner's visual mode".
"""

from __future__ import annotations

import http.server
import shutil
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CHROMIUM_PATH = Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
DEMO_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "demo"

playwright_sync_api = pytest.importorskip(
    "playwright.sync_api",
    reason="playwright is not installed; skipping web e2e tests",
)

if not CHROMIUM_PATH.exists():
    pytest.skip(
        f"pinned Chromium not found at {CHROMIUM_PATH}; skipping web e2e tests",
        allow_module_level=True,
    )

sync_playwright = playwright_sync_api.sync_playwright


# The demo fixture's `start` scene ends in a `choice`; we add a third,
# unconditional option here that takes the player into a new scene
# that opens `mode inner`, shows one line, then jumps onward to
# `ending` (an existing terminal scene) so gotoScene's mode reset is
# what puts the game back into "default" — the runner has no other
# code path that would do it, so this is the real behavior, not a
# test-only shortcut.
MODE_SCENE_TEXT = """

== inner_room
mode inner
> The room holds still around you.
-> ending
"""

CHOICE_LINE = '    "Call Clipi in on the terminal." -> call_clipi\n'
NEW_CHOICE_LINE = (
    '    "Call Clipi in on the terminal." -> call_clipi\n'
    '    "Step into the inner room." -> inner_room\n'
)


def _build_story_with_mode_scene(tmp_path: Path) -> Path:
    story_dir = tmp_path / "story"
    shutil.copytree(DEMO_FIXTURE, story_dir)
    scene_path = story_dir / "demo.scene"
    text = scene_path.read_text(encoding="utf-8")
    assert CHOICE_LINE in text, "demo.scene's start choice changed shape"
    text = text.replace(CHOICE_LINE, NEW_CHOICE_LINE, 1)
    text += MODE_SCENE_TEXT
    scene_path.write_text(text, encoding="utf-8")
    return story_dir


@pytest.fixture(scope="module")
def dist_dir(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("mode-web")
    story_dir = _build_story_with_mode_scene(tmp_path)
    out_dir = tmp_path / "dist"
    from linkloader.build import build

    build(story_dir, out_dir, root=REPO_ROOT)
    return out_dir


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # noqa: D401 - silence per-request logging
        pass


@pytest.fixture(scope="module")
def base_url(dist_dir):
    port = _free_port()
    handler = lambda *args, **kwargs: _QuietHandler(*args, directory=str(dist_dir), **kwargs)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        httpd.shutdown()
        thread.join(timeout=5)


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(CHROMIUM_PATH))
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    pg = ctx.new_page()
    yield pg
    ctx.close()


def _pick_inner_room(options):
    for i, text in enumerate(options):
        if "inner room" in text:
            return i
    return 0


def test_mode_sets_data_mode_and_resets_after_jump(page, base_url):
    page.goto(base_url + "/")
    page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")

    assert page.get_attribute("#game", "data-mode") == "default"

    # Reach the start scene's choice (two dialogue/narration lines
    # come first) and step into the inner room.
    for _ in range(10):
        if page.is_visible("#choices-wrap"):
            break
        if page.is_visible("#dialogue-box"):
            page.click("#dialogue-box")
            page.wait_for_timeout(20)
    page.wait_for_selector("#choices-wrap", state="visible")
    buttons = page.query_selector_all("#choices-list button")
    texts = [b.inner_text() for b in buttons]
    buttons[_pick_inner_room(texts)].click()
    page.wait_for_timeout(20)

    assert page.get_attribute("#game", "data-mode") == "inner"
    label = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label == "inner_room"

    # Advance past the narration line, which jumps to `ending` (a
    # terminal scene): gotoScene resets data-mode to "default" on
    # every scene entry, mode or not.
    page.click("#dialogue-box")
    page.wait_for_timeout(20)

    assert page.get_attribute("#game", "data-mode") == "default"
    label = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label == "ending"
