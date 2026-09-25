#!/usr/bin/env python3
"""Capture the screenshots the style guide shows, from a real build.

Usage:
    python -m linkloader build story/ -o dist/
    python tools/guide/capture.py dist/ web/guide/shots/

Needs Playwright. Set CHROMIUM to a Chromium binary if Playwright's own
browser is not installed. Every shot uses a fixed seed, so a rerun gives
the same dice.
"""
import functools
import http.server
import os
import socket
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
DESKTOP = {"width": 1100, "height": 760}
PHONE = {"width": 390, "height": 844}


def serve(directory):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    handler.log_message = lambda *a: None
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{port}"


def advance_until(page, visible, choose=lambda texts: 0, steps=400):
    for _ in range(steps):
        el = page.query_selector(visible)
        if el and el.is_visible():
            return
        if page.is_visible("#dialogue-box"):
            page.keyboard.press("Space")
        elif page.is_visible("#choices-wrap"):
            buttons = page.query_selector_all("#choices-list button")
            buttons[choose([b.inner_text() for b in buttons])].click()
        elif page.is_visible("#check-panel"):
            page.click("#check-actions .btn-primary")
        else:
            page.wait_for_timeout(20)
    raise RuntimeError(f"never reached {visible}")


def cowboy_then_head_out(texts):
    for i, t in enumerate(texts):
        if "dirt, fixing" in t:
            return i
    for i, t in enumerate(texts):
        if "Head out" in t:
            return i
    return 0


def room_chooser(texts):
    """Carries the player from the start down to and through the room
    (docs/plans/wave2.md sections 2 and 4): head out without Clipi,
    leave the rustler brand alone, talk Clipi down with the base-case
    phrase, then open the chest before the window."""
    for i, t in enumerate(texts):
        if "Head out" in t:
            return i
    for i, t in enumerate(texts):
        if "Leave it. It isn't cargo." in t:
            return i
    for i, t in enumerate(texts):
        if "Say fen" in t:
            return i
    for i, t in enumerate(texts):
        if "Open the chest of drawers." in t:
            return i
    return 0


def answer_text(root, puzzle_id):
    return (root / "puzzles" / puzzle_id / "answer.rill").read_text(encoding="utf-8")


def walk_to_room_hub(page, base, root, seed=1):
    """Plays from `start` down through the found-document scene to
    `room_hub` (see story/03-clipi.scene and story/03b-room.scene),
    passing decode-buoy and count-crew and skipping the optional
    read-brand puzzle."""
    page.goto(f"{base}/?seed={seed}")
    page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")
    answers = {"decode-buoy": answer_text(root, "decode-buoy"), "count-crew": answer_text(root, "count-crew")}
    for _ in range(400):
        if page.evaluate("() => window.__linkloaderGame.currentLabel") == "room_hub" and page.is_visible(
            "#choices-wrap"
        ):
            return
        if page.is_visible("#puzzle-panel"):
            title = page.inner_text("#puzzle-title").lower()
            pid = next(p for p in answers if p in title)
            page.fill("#puzzle-editor", answers[pid])
            page.click("#puzzle-check-btn")
            page.wait_for_function("() => document.getElementById('puzzle-panel').hidden === true")
            continue
        if page.is_visible("#dialogue-box"):
            page.click("#dialogue-box")
            page.wait_for_timeout(15)
            continue
        if page.is_visible("#choices-wrap"):
            buttons = page.query_selector_all("#choices-list button")
            buttons[room_chooser([b.inner_text() for b in buttons])].click()
            page.wait_for_timeout(15)
            continue
        if page.is_visible("#check-panel"):
            page.click("#check-actions .btn-primary")
            continue
        page.wait_for_timeout(20)
    raise RuntimeError("gave up waiting for room_hub")


def shot(page, out, name):
    page.wait_for_timeout(150)
    page.locator("#game").screenshot(path=str(out / f"{name}.jpg"), quality=82, type="jpeg")


def main(dist, out):
    out.mkdir(parents=True, exist_ok=True)
    server, base = serve(dist)
    launch = {"executable_path": os.environ["CHROMIUM"]} if os.environ.get("CHROMIUM") else {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**launch)
            for size, suffix in [(DESKTOP, ""), (PHONE, "-phone")]:
                page = browser.new_context(viewport=size).new_page()
                page.goto(f"{base}/?seed=7")
                page.evaluate("() => localStorage.clear()")
                page.goto(f"{base}/?seed=7")
                page.wait_for_selector("#dialogue-box", state="visible")
                page.keyboard.press("Space")
                advance_until(page, "#dialogue-text:has-text('')")
                shot(page, out, "dialogue" + suffix)
                advance_until(page, "#choices-wrap")
                shot(page, out, "choices" + suffix)
                advance_until(page, "#puzzle-panel", cowboy_then_head_out)
                page.fill("#puzzle-editor", "(stake answer (seal (signal star dust drift harbor)))")
                page.click("#puzzle-check-btn")
                shot(page, out, "puzzle" + suffix)
                page.click("#puzzle-lexicon-btn")
                shot(page, out, "lexicon" + suffix)
                page.click("#lexicon-close-btn")
                page.fill("#puzzle-editor", "(stake answer (seal (signal star dust drift home)))")
                page.click("#puzzle-check-btn")
                advance_until(page, "#check-panel", cowboy_then_head_out)
                shot(page, out, "check" + suffix)

                # The inner stratum: the found document and the room
                # (docs/plans/wave2.md sections 2 and 4).
                page.evaluate("() => localStorage.clear()")
                page.goto(f"{base}/?seed=1")
                page.wait_for_selector("#dialogue-box, #choices-wrap", state="visible")
                found_answers = {
                    "decode-buoy": answer_text(ROOT, "decode-buoy"),
                    "count-crew": answer_text(ROOT, "count-crew"),
                }
                for _ in range(400):
                    if page.evaluate("() => window.__linkloaderGame.currentLabel") == "found_document":
                        break
                    if page.is_visible("#puzzle-panel"):
                        title = page.inner_text("#puzzle-title").lower()
                        pid = next(p for p in found_answers if p in title)
                        page.fill("#puzzle-editor", found_answers[pid])
                        page.click("#puzzle-check-btn")
                        page.wait_for_function(
                            "() => document.getElementById('puzzle-panel').hidden === true"
                        )
                        continue
                    if page.is_visible("#dialogue-box"):
                        page.click("#dialogue-box")
                        page.wait_for_timeout(15)
                        continue
                    if page.is_visible("#choices-wrap"):
                        buttons = page.query_selector_all("#choices-list button")
                        buttons[room_chooser([b.inner_text() for b in buttons])].click()
                        page.wait_for_timeout(15)
                        continue
                    if page.is_visible("#check-panel"):
                        page.click("#check-actions .btn-primary")
                        continue
                    page.wait_for_timeout(20)
                shot(page, out, "found-document" + suffix)

                page.evaluate("() => localStorage.clear()")
                walk_to_room_hub(page, base, ROOT, seed=1)
                shot(page, out, "room" + suffix)
            browser.close()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
