"""Export a parsed Story (plus cast and assets) to the JSON schema
documented in docs/scene-format.md, "The JSON export schema".
"""

from __future__ import annotations

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
