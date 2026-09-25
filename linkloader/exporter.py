"""Export a parsed Story (plus cast and assets) to the JSON schema
documented in docs/scene-format.md, "The JSON export schema".

Two extra pieces used only by `linkloader build` (see build.py) live
here too, kept separate from `export_story` so its return shape never
changes for the plain `python -m linkloader export` command:

- `build_ladder()` — the 4dF outcome ladder, read out of
  `linkloader/dice.py` by calling its own `tier_for`, so the web
  runner's copy can never drift from the Python one.
- `build_puzzles_data()` — per-puzzle prompt/starter/hint/cases for
  the web puzzle panel, per contract C2.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .dice import DIFFICULTY_LADDER, FATE_FACES, tier_for
from .model import (
    Bg,
    CheckStmt,
    ChoiceStmt,
    Condition,
    Hide,
    IfStmt,
    Jump,
    Line,
    Narration,
    PuzzleStmt,
    SetStmt,
    Show,
    Story,
)


def _condition_to_dict(cond: Condition | None):
    if cond is None:
        return None
    return {"flag": cond.flag, "op": cond.op, "value": cond.value}


def _statement_to_dict(stmt) -> dict:
    if isinstance(stmt, Bg):
        return {"kind": "bg", "name": stmt.name}
    if isinstance(stmt, Show):
        return {
            "kind": "show",
            "sprite": stmt.sprite,
            "expression": stmt.expression,
            "position": stmt.position,
        }
    if isinstance(stmt, Hide):
        return {"kind": "hide", "sprite": stmt.sprite}
    if isinstance(stmt, Line):
        return {"kind": "line", "speaker": stmt.speaker, "text": stmt.text}
    if isinstance(stmt, Narration):
        return {"kind": "narration", "text": stmt.text}
    if isinstance(stmt, SetStmt):
        return {
            "kind": "set",
            "assignments": [
                {"flag": a.flag, "op": a.op, "value": a.value} for a in stmt.assignments
            ],
        }
    if isinstance(stmt, IfStmt):
        return {
            "kind": "if",
            "condition": _condition_to_dict(stmt.condition),
            "then": [_statement_to_dict(s) for s in stmt.then],
            "else": [_statement_to_dict(s) for s in stmt.else_],
        }
    if isinstance(stmt, ChoiceStmt):
        return {
            "kind": "choice",
            "options": [
                {
                    "text": o.text,
                    "target": o.target,
                    "condition": _condition_to_dict(o.condition),
                }
                for o in stmt.options
            ],
        }
    if isinstance(stmt, CheckStmt):
        return {
            "kind": "check",
            "stat": stmt.stat,
            "difficulty": stmt.difficulty,
            "outcomes": dict(stmt.outcomes),
        }
    if isinstance(stmt, PuzzleStmt):
        return {"kind": "puzzle", "id": stmt.puzzle_id, "outcomes": dict(stmt.outcomes)}
    if isinstance(stmt, Jump):
        return {"kind": "jump", "target": stmt.target}
    raise TypeError(f"unknown statement type: {type(stmt)!r}")


def export_story(story: Story, cast: dict, assets: dict) -> dict:
    return {
        "start": story.start,
        "scenes": {
            label: {"statements": [_statement_to_dict(s) for s in scene.statements]}
            for label, scene in story.scenes.items()
        },
        "cast": cast,
        "assets": assets,
    }


# ---------------------------------------------------------------------------
# `linkloader build` extras: the ladder and the puzzle data.


def build_ladder() -> dict:
    """The 4dF outcome ladder, derived by calling `dice.tier_for`
    itself rather than copying its threshold numbers here — so this
    can never silently drift from linkloader/dice.py.

    `tier_for(total, difficulty)` only depends on `total - difficulty`
    (the "shift"), so probing it at difficulty 0 finds each tier's
    minimum qualifying shift.
    """
    style_min = next(s for s in range(0, 50) if tier_for(s, 0) == "style")
    success_min = next(s for s in range(0, 50) if tier_for(s, 0) == "success")
    tie_shift = next(s for s in range(-50, 50) if tier_for(s, 0) == "tie")
    return {
        "faces": list(FATE_FACES),
        "dice_count": 4,
        "difficulties": dict(DIFFICULTY_LADDER),
        # Checked by the runner in this order; "fail" is whatever is left.
        "tiers": [
            {"tier": "style", "min_shift": style_min},
            {"tier": "success", "min_shift": success_min},
            {"tier": "tie", "shift": tie_shift},
            {"tier": "fail"},
        ],
    }


def _md_to_html(text: str) -> str:
    """A deliberately small Markdown-to-HTML pass: paragraphs, ```
    fences, and inline `code`. Enough for a puzzle prompt; not a
    general Markdown renderer."""
    import html as _html

    lines = text.strip("\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_para():
        if para:
            joined = " ".join(para).strip()
            if joined:
                out.append(f"<p>{_inline(joined)}</p>")
            para.clear()

    def _inline(s: str) -> str:
        s = _html.escape(s)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                out.append(
                    "<pre><code>" + _html.escape("\n".join(code_lines)) + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                flush_para()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped == "":
            flush_para()
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_para()
            level = min(len(heading.group(1)) + 2, 6)  # ## -> h4, ### -> h5
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue
        para.append(stripped)
    flush_para()
    if in_code:  # unterminated fence; emit what we have rather than lose it
        out.append("<pre><code>" + _html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def _parse_puzzle_md(text: str) -> tuple[str, str, str | None]:
    """Splits a puzzle.md into (title, prompt_html, hint_html_or_None).

    The title is the leading `# ...` line. A `## Hint` section, if
    present, is pulled out of the prompt body and returned separately
    (contract C2: "hint" is null when the section is absent).
    """
    lines = text.split("\n")
    title = ""
    body_start = 0
    if lines and lines[0].strip().startswith("# "):
        title = lines[0].strip()[2:].strip()
        body_start = 1
    body = "\n".join(lines[body_start:])

    hint_match = re.search(r"(?m)^##\s+Hint\s*$", body)
    if hint_match is None:
        return title, _md_to_html(body), None

    prompt_body = body[: hint_match.start()]
    hint_body = body[hint_match.end() :]
    # Stop the hint section at the next heading of the same or higher level.
    next_heading = re.search(r"(?m)^#{1,2}\s+\S", hint_body)
    if next_heading:
        hint_body = hint_body[: next_heading.start()]
    return title, _md_to_html(prompt_body), _md_to_html(hint_body)


def _parse_lexicon_table_rows(block: str) -> list[list[str]]:
    """Pulls the data rows out of one Markdown table (a run of `|...|`
    lines): drops the header row and the `|---|---|` separator row,
    and un-backtick/strip every cell. Tolerant of extra whitespace and
    of a table that isn't perfectly column-aligned."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue  # the `|---|---|` separator row
        rows.append([c.strip("`").strip() for c in cells])
    return rows[1:] if len(rows) > 1 else []  # drop the header row


def build_lexicon(text: str) -> list[dict]:
    """Parses `puzzles/rill/lexicon.md` into a flat list of
    {"word", "gloss", "kind", "scheme"} entries: "grammar" rows carry
    the Scheme primitive they alias (e.g. `car`), "theme" rows carry
    `scheme: None`. Robust to the exact heading wording (matched by
    prefix, case-insensitively) and to `(12)`/`(8)`-style counts in
    the heading, so a lexicon edit that adds or renames a word still
    parses."""
    entries: list[dict] = []
    for heading, body in re.findall(r"(?m)^##\s+(.+?)\s*$\n((?:(?!^##\s).*\n?)*)", text):
        rows = _parse_lexicon_table_rows(body)
        if not rows:
            continue
        heading_lower = heading.strip().lower()
        if heading_lower.startswith("grammar"):
            for row in rows:
                if len(row) < 3:
                    continue
                word, scheme, gloss = row[0], row[1], row[2]
                if not word:
                    continue
                entries.append({"word": word, "gloss": gloss, "kind": "grammar", "scheme": scheme})
        elif heading_lower.startswith("thematic") or heading_lower.startswith("theme"):
            for row in rows:
                if len(row) < 2:
                    continue
                word, gloss = row[0], row[1]
                if not word:
                    continue
                entries.append({"word": word, "gloss": gloss, "kind": "theme", "scheme": None})
    return entries


def build_puzzles_data(puzzles_dir: Path, puzzle_ids) -> dict:
    """Per contract C2: {"<id>": {"id", "title", "prompt", "starter",
    "hint", "cases"}} for each id in `puzzle_ids`."""
    cases_path = puzzles_dir / "cases.json"
    all_cases = {}
    if cases_path.exists():
        all_cases = json.loads(cases_path.read_text(encoding="utf-8")).get("puzzles", {})

    out: dict = {}
    for puzzle_id in puzzle_ids:
        puzzle_dir = puzzles_dir / puzzle_id
        md_path = puzzle_dir / "puzzle.md"
        starter_path = puzzle_dir / "starter.rill"

        md_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        title, prompt_html, hint_html = _parse_puzzle_md(md_text)
        starter = starter_path.read_text(encoding="utf-8") if starter_path.exists() else ""

        out[puzzle_id] = {
            "id": puzzle_id,
            "title": title or puzzle_id,
            "prompt": prompt_html,
            "starter": starter,
            "hint": hint_html,
            "cases": all_cases.get(puzzle_id, []),
        }
    return out
