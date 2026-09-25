"""End-to-end tests for the web build (dist/), driven with Playwright.

Builds a fresh dist/ into a temp directory, serves it with
`python -m http.server`, and drives it with a real Chromium. Skips
cleanly (pytest.skip) if Playwright or the pinned Chromium build is
missing, so the rest of the suite still runs where those are absent.

See AGENTS.md "Check your work" and the SHARED CONTRACTS note in
web/runner.js and web/rill/rill.js for what this checks.
"""

from __future__ import annotations

import http.server
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CHROMIUM_PATH = Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

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


# ---------------------------------------------------------------------------
# Build + serve fixtures.


@pytest.fixture(scope="session")
def dist_dir(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("dist")
    subprocess.run(
        [sys.executable, "-m", "linkloader", "build", "story/", "-o", str(out_dir)],
        cwd=REPO_ROOT,
        check=True,
    )
    return out_dir


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # noqa: D401 - silence per-request logging
        pass


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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


# ---------------------------------------------------------------------------
# Driving helpers.

MAX_STEPS = 400


def advance_until(page, selector, choose=None, max_steps=MAX_STEPS):
    """Drives the game forward (Space for dialogue, clicking choices
    and check "Continue" buttons) until `selector` is visible, or
    raises after max_steps.

    `choose(option_texts) -> int` picks a choice's index (0-based) when
    a choice panel appears; defaults to always picking the first option.
    """
    choose = choose or (lambda _options: 0)
    for _ in range(max_steps):
        target = page.query_selector(selector)
        if target and target.is_visible():
            return
        if page.is_visible("#dialogue-box"):
            page.keyboard.press("Space")
            continue
        if page.is_visible("#choices-wrap"):
            buttons = page.query_selector_all("#choices-list button")
            texts = [b.inner_text() for b in buttons]
            idx = choose(texts)
            buttons[idx].click()
            continue
        if page.is_visible("#check-panel"):
            page.click("#check-actions .btn-primary")
            continue
        # Nothing recognized is showing yet (e.g. mid-transition); give
        # the page a moment and re-check.
        page.wait_for_timeout(20)
    raise AssertionError(f"gave up waiting for {selector!r} after {max_steps} steps")


def goto(page, base_url, seed=None):
    url = base_url + "/"
    if seed is not None:
        url += f"?seed={seed}"
    page.goto(url)


def pick_head_out(options):
    for i, text in enumerate(options):
        if "Head out" in text:
            return i
    return 0


def pick_cowboy_origin_then_head_out(options):
    for i, text in enumerate(options):
        if "dirt, fixing" in text:  # the cowboy origin option
            return i
    return pick_head_out(options)


# ---------------------------------------------------------------------------
# Tests.


def _is_environment_noise(text: str) -> bool:
    """Two failures are artifacts of this sandbox, not the app: the
    proxy blocks the Google Fonts preconnect with an untrusted cert,
    and Chromium always requests /favicon.ico whether or not one
    exists."""
    return "ERR_CERT_AUTHORITY_INVALID" in text or "404" in text


def test_game_loads_with_no_console_errors(page, base_url):
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    goto(page, base_url)
    page.wait_for_selector("#dialogue-box", state="visible")
    real_errors = [e for e in errors if not _is_environment_noise(e)]
    assert real_errors == [], f"console/page errors on load: {real_errors}"


def test_click_and_keys_advance_dialogue(page, base_url):
    goto(page, base_url)
    page.wait_for_selector("#dialogue-box", state="visible")
    first_text = page.inner_text("#dialogue-text")

    # A click on the dialogue box advances it.
    page.click("#dialogue-box")
    page.wait_for_timeout(20)
    second_text = page.inner_text("#dialogue-text")
    assert second_text != first_text

    # Space/Enter also advance it.
    page.keyboard.press("Space")
    page.wait_for_timeout(20)
    third_text = page.inner_text("#dialogue-text")
    assert third_text != second_text

    page.keyboard.press("Enter")
    page.wait_for_timeout(20)
    fourth_text = page.inner_text("#dialogue-text")
    assert fourth_text != third_text


def test_check_shows_four_dice_and_ladder_result(page, base_url):
    # The first "check" statement (see story/02-sabotage.scene) comes
    # right after decode-buoy's puzzle -- pass the reference answer to
    # get there, then let the check panel appear.
    _reach_decode_buoy(page, base_url, seed=1)
    answer = (REPO_ROOT / "puzzles" / "decode-buoy" / "answer.rill").read_text(
        encoding="utf-8"
    )
    page.fill("#puzzle-editor", answer)
    page.click("#puzzle-check-btn")
    advance_until(page, "#check-panel")

    dice = page.query_selector_all("#dice-row .die")
    assert len(dice) == 4
    result_text = page.inner_text("#check-result")
    assert "->" in result_text
    tier = result_text.split("->")[-1].strip()
    assert tier in {"STYLE", "SUCCESS", "TIE", "FAIL"}


def test_check_shows_a_nonzero_stat_after_the_origin_choice(page, base_url):
    # Picking the cowboy origin sets cowboy=2 (see story/01-arrival.scene);
    # story/02-sabotage.scene's first check is "check cowboy vs 2", so
    # the check panel must show a nonzero cowboy stat, not the old
    # hardcoded 0.
    goto(page, base_url, seed=1)
    advance_until(page, "#puzzle-panel", choose=pick_cowboy_origin_then_head_out)
    answer = (REPO_ROOT / "puzzles" / "decode-buoy" / "answer.rill").read_text(
        encoding="utf-8"
    )
    page.fill("#puzzle-editor", answer)
    page.click("#puzzle-check-btn")
    advance_until(page, "#check-panel")

    title = page.inner_text("#check-title")
    assert "cowboy +2" in title.lower()
    result_text = page.inner_text("#check-result")
    assert "cowboy +2" in result_text


def test_lexicon_panel_shows_grammar_and_theme_words_without_losing_editor_text(
    page, base_url
):
    _reach_decode_buoy(page, base_url, seed=1)
    page.fill("#puzzle-editor", "(stake answer (seal (draft draft)))")

    page.click("#puzzle-lexicon-btn")
    page.wait_for_selector("#lexicon-panel", state="visible")
    assert page.inner_text("#lexicon-grammar-body").strip() != ""
    assert page.inner_text("#lexicon-theme-body").strip() != ""
    assert "signal" in page.inner_text("#lexicon-theme-body")

    # Opening the lexicon never touches what the player already typed.
    assert page.input_value("#puzzle-editor") == "(stake answer (seal (draft draft)))"

    page.click("#lexicon-close-btn")
    assert page.is_hidden("#lexicon-panel")
    assert page.input_value("#puzzle-editor") == "(stake answer (seal (draft draft)))"


def _reach_decode_buoy(page, base_url, seed=None):
    goto(page, base_url, seed=seed)
    advance_until(page, "#puzzle-panel", choose=pick_head_out)


def test_reach_first_puzzle_and_pass_with_reference_answer(page, base_url):
    _reach_decode_buoy(page, base_url, seed=1)
    assert page.inner_text("#puzzle-title") != ""

    answer = (REPO_ROOT / "puzzles" / "decode-buoy" / "answer.rill").read_text(
        encoding="utf-8"
    )
    page.fill("#puzzle-editor", answer)
    page.click("#puzzle-check-btn")

    # A passing answer moves straight into the pass branch's scene,
    # hiding the puzzle panel and showing its first line/narration.
    page.wait_for_function(
        "() => document.getElementById('puzzle-panel').hidden === true"
    )
    label = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label == "transmission_clear"


def test_three_wrong_answers_reach_lockout(page, base_url):
    _reach_decode_buoy(page, base_url, seed=2)

    for _ in range(3):
        page.fill("#puzzle-editor", "(stake answer (seal (nope nope nope nope nope)))")
        page.click("#puzzle-check-btn")
        page.wait_for_timeout(20)

    page.wait_for_function(
        "() => document.getElementById('puzzle-panel').hidden === true"
    )
    label = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label == "transmission_garbled"


def test_save_and_continue_survives_reload(page, base_url):
    goto(page, base_url)
    page.wait_for_selector("#dialogue-box", state="visible")
    # Advance a couple of beats so the saved label isn't just "start".
    page.click("#dialogue-box")
    page.wait_for_timeout(20)
    page.click("#dialogue-box")
    page.wait_for_timeout(20)
    label_before = page.evaluate("() => window.__linkloaderGame.currentLabel")

    page.reload()
    page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")
    label_after = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label_after == label_before


def test_save_is_a_scene_entry_snapshot(page, base_url):
    """A reload replays the scene from its start with the flags, Fate and
    dice state it had on entry, so nothing in the scene applies twice."""
    goto(page, base_url)
    page.wait_for_selector("#dialogue-box", state="visible")
    saved = page.evaluate("() => JSON.parse(localStorage.getItem('linkloader-save-v1'))")
    assert isinstance(saved["rngState"], int)
    entry_flags = saved["flags"]

    # Change flags and dice mid-scene; the save must not move.
    page.evaluate(
        "() => { const g = window.__linkloaderGame; g.flags.probe = 7; g.rng(); g.rng(); }"
    )
    after = page.evaluate("() => JSON.parse(localStorage.getItem('linkloader-save-v1'))")
    assert after == saved
    page.reload()
    page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")
    flags = page.evaluate("() => window.__linkloaderGame.flags")
    assert flags == entry_flags


def test_no_horizontal_scroll_at_mobile_width(browser, base_url):
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    try:
        goto(page, base_url)
        page.wait_for_selector("#dialogue-box", state="visible")
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1"
        )
        assert not overflow, "page has horizontal scroll at 390x844"
    finally:
        ctx.close()


def test_stage_carries_over_between_scenes_and_survives_reload(page, base_url):
    """Scenes do not clear the stage; only show, hide and bg change it.
    The origin choice leads to a scene with no show of its own, and Slim
    must still be on stage there, and after a reload."""
    goto(page, base_url, seed=3)
    page.evaluate("() => localStorage.clear()")
    goto(page, base_url, seed=3)
    advance_until(page, "#choices-wrap")
    page.query_selector_all("#choices-list button")[0].click()
    page.wait_for_timeout(50)
    label = page.evaluate("() => window.__linkloaderGame.currentLabel")
    assert label != "start"
    assert page.is_visible("#sprite-left")
    bg = page.evaluate("() => document.getElementById('bg-layer').style.backgroundImage")
    assert "assets/" in bg

    # Reload without the seed so the save is used.
    page.goto(base_url + "/")
    page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")
    assert page.is_visible("#sprite-left")
    assert "assets/" in page.evaluate("() => document.getElementById('bg-layer').style.backgroundImage")
