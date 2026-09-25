"""Parser for `.scene` files. See docs/scene-format.md for the grammar.

`parse_file(path)` returns a list of `model.Scene` found in that one
file. It never looks at other files, `cast.toml`, or `assets.toml` —
those checks belong to the validator, which runs after every file is
parsed and the whole story exists.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .errors import ParseError
from .model import (
    Assignment,
    Bg,
    CheckStmt,
    ChoiceOption,
    ChoiceStmt,
    Condition,
    Hide,
    IfStmt,
    Jump,
    Line,
    Narration,
    Pos,
    PuzzleStmt,
    Scene,
    SetStmt,
    Show,
)

IDENT = r"[a-z][a-z0-9_]*"
PUZZLE_ID = r"[a-z0-9][a-z0-9_-]*"

SCENE_RE = re.compile(rf"^==\s*({IDENT})\s*$")
BG_RE = re.compile(rf"^bg\s+({IDENT})\s*$")
SHOW_RE = re.compile(rf"^show\s+({IDENT})\s+({IDENT})(?:\s+({IDENT}))?\s*$")
HIDE_RE = re.compile(rf"^hide\s+({IDENT})\s*$")
DIALOGUE_RE = re.compile(rf"^({IDENT}):\s(.*)$")
JUMP_RE = re.compile(rf"^->\s*({IDENT})\s*$")
CHECK_RE = re.compile(rf"^check\s+({IDENT})\s+vs\s+(\d+)\s*$")
PUZZLE_RE = re.compile(rf"^puzzle\s+({PUZZLE_ID})\s*$")
OUTCOME_CHECK_RE = re.compile(rf"^(style|success|tie|fail)\s*->\s*({IDENT})\s*$")
OUTCOME_PUZZLE_RE = re.compile(rf"^(pass|lockout)\s*->\s*({IDENT})\s*$")
OPTION_RE = re.compile(r'^"([^"]*)"\s*->\s*(' + IDENT + r")(?:\s*\[if\s+(.+)\])?\s*$")
ASSIGN_RE = re.compile(rf"^\s*({IDENT})\s*(=|\+=|-=)\s*(true|false|-?\d+)\s*$")
COND_NOT_RE = re.compile(rf"^not\s+({IDENT})\s*$")
COND_CMP_RE = re.compile(rf"^({IDENT})\s*(==|!=|>=|<=|>|<)\s*(true|false|-?\d+)\s*$")
COND_TRUTHY_RE = re.compile(rf"^({IDENT})\s*$")

VALID_STATS = ("cosmonaut", "cowboy", "coder")
VALID_POSITIONS = ("left", "center", "right")


@dataclass(frozen=True)
class _Line:
    file: str
    lineno: int
    indent: int
    text: str


def _err(line: _Line, code: str, message: str) -> ParseError:
    return ParseError(line.file, line.lineno, line.indent + 1, code, message)


def _parse_value(s: str):
    if s == "true":
        return True
    if s == "false":
        return False
    return int(s)


def _load_lines(path: str) -> list[_Line]:
    lines: list[_Line] = []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.rstrip("\n").rstrip("\r")
            if raw.strip() == "":
                continue
            indent_str = raw[: len(raw) - len(raw.lstrip(" "))]
            if "\t" in raw[: len(indent_str) + 1]:
                raise ParseError(
                    path, lineno, 1, "BadIndent", "tabs are not allowed; use spaces"
                )
            indent = len(indent_str)
            text = raw[indent:]
            if text.startswith("#"):
                continue
            lines.append(_Line(path, lineno, indent, text))
    return lines


def parse_file(path: str) -> list[Scene]:
    lines = _load_lines(path)
    scenes: list[Scene] = []
    idx = 0
    n = len(lines)
    if n == 0:
        return scenes
    while idx < n:
        line = lines[idx]
        if line.indent != 0:
            raise _err(line, "BadIndent", "expected a scene header (`== label`) at column 0")
        m = SCENE_RE.match(line.text)
        if not m:
            raise _err(line, "ExpectedSceneHeader", f"expected `== label`, got: {line.text!r}")
        label = m.group(1)
        header_pos = Pos(path, line.lineno, 1)
        idx += 1
        stmts, idx = _parse_block(lines, idx, 0)
        scenes.append(Scene(label=label, statements=stmts, pos=header_pos))
    return scenes


def _parse_block(lines: list[_Line], idx: int, indent: int) -> tuple[list, int]:
    stmts = []
    n = len(lines)
    while idx < n and lines[idx].indent == indent and not lines[idx].text.startswith("=="):
        stmt, idx = _parse_statement(lines, idx, indent)
        stmts.append(stmt)
    if idx < n and lines[idx].indent > indent and not lines[idx].text.startswith("=="):
        raise _err(
            lines[idx],
            "BadIndent",
            f"unexpected indent ({lines[idx].indent} spaces; expected {indent})",
        )
    return stmts, idx


def _block_indent(lines: list[_Line], idx: int, parent_indent: int) -> int | None:
    if idx < len(lines) and lines[idx].indent > parent_indent:
        return lines[idx].indent
    return None


def _parse_condition(text: str, line: _Line) -> Condition:
    text = text.strip()
    m = COND_NOT_RE.match(text)
    if m:
        return Condition(flag=m.group(1), op="not")
    m = COND_CMP_RE.match(text)
    if m:
        flag, op, value = m.groups()
        if op in (">=", "<=", ">", "<") and value in ("true", "false"):
            raise _err(line, "BadCondition", f"{op} compares integers, not {value}: {text!r}")
        return Condition(flag=flag, op=op, value=_parse_value(value))
    m = COND_TRUTHY_RE.match(text)
    if m:
        return Condition(flag=m.group(1), op="truthy")
    raise _err(line, "BadCondition", f"malformed condition: {text!r}")


def _parse_statement(lines: list[_Line], idx: int, indent: int):
    line = lines[idx]
    text = line.text
    pos = Pos(line.file, line.lineno, indent + 1)

    if text == "choice":
        return _parse_choice(lines, idx + 1, indent, pos)

    if text.startswith("if ") or text == "if":
        cond_text = text[2:].strip()
        if not cond_text:
            raise _err(line, "BadCondition", "`if` needs a condition")
        cond = _parse_condition(cond_text, line)
        return _parse_if(lines, idx + 1, indent, cond, pos)

    if text.startswith("check "):
        m = CHECK_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed check: {text!r}")
        stat, difficulty = m.groups()
        if stat not in VALID_STATS:
            raise _err(
                line, "UnknownStat", f"unknown stat {stat!r}; expected one of {VALID_STATS}"
            )
        return _parse_check(lines, idx + 1, indent, stat, int(difficulty), pos)

    if text.startswith("puzzle "):
        m = PUZZLE_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed puzzle: {text!r}")
        return _parse_puzzle(lines, idx + 1, indent, m.group(1), pos)

    if text.startswith("bg "):
        m = BG_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed bg: {text!r}")
        return Bg(name=m.group(1), pos=pos), idx + 1

    if text.startswith("show "):
        m = SHOW_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed show: {text!r}")
        sprite, expression, position = m.groups()
        position = position or "center"
        if position not in VALID_POSITIONS:
            raise _err(
                line,
                "BadStatement",
                f"unknown position {position!r}; expected one of {VALID_POSITIONS}",
            )
        return Show(sprite=sprite, expression=expression, position=position, pos=pos), idx + 1

    if text.startswith("hide "):
        m = HIDE_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed hide: {text!r}")
        return Hide(sprite=m.group(1), pos=pos), idx + 1

    if text.startswith("set "):
        return _parse_set(text[4:], line, pos), idx + 1

    if text.startswith("> "):
        return Narration(text=text[2:], pos=pos), idx + 1

    if text.startswith("->"):
        m = JUMP_RE.match(text)
        if not m:
            raise _err(line, "BadStatement", f"malformed jump: {text!r}")
        return Jump(target=m.group(1), pos=pos), idx + 1

    m = DIALOGUE_RE.match(text)
    if m:
        return Line(speaker=m.group(1), text=m.group(2), pos=pos), idx + 1

    raise _err(line, "UnknownStatement", f"unrecognized statement: {text!r}")


def _parse_set(rest: str, line: _Line, pos: Pos) -> SetStmt:
    parts = [p.strip() for p in rest.split(",")]
    assignments = []
    for part in parts:
        m = ASSIGN_RE.match(part)
        if not m:
            raise _err(line, "BadValue", f"malformed assignment: {part!r}")
        flag, op, value = m.groups()
        parsed_value = _parse_value(value)
        is_plain_int = isinstance(parsed_value, int) and not isinstance(parsed_value, bool)
        if op in ("+=", "-=") and not is_plain_int:
            raise _err(line, "BadValue", f"`{op}` needs an integer value, got {value!r}")
        assignments.append(Assignment(flag=flag, op=op, value=parsed_value))
    if not assignments:
        raise _err(line, "BadValue", "`set` needs at least one assignment")
    return SetStmt(assignments=tuple(assignments), pos=pos)


def _parse_choice(lines: list[_Line], idx: int, indent: int, pos: Pos):
    child_indent = _block_indent(lines, idx, indent)
    if child_indent is None:
        raise _err(lines[idx - 1] if idx > 0 else lines[idx], "EmptyChoice", "`choice` has no options")
    options = []
    n = len(lines)
    while idx < n and lines[idx].indent == child_indent:
        oline = lines[idx]
        m = OPTION_RE.match(oline.text)
        if not m:
            raise _err(oline, "BadChoiceOption", f"malformed choice option: {oline.text!r}")
        otext, target, cond_text = m.groups()
        cond = _parse_condition(cond_text, oline) if cond_text else None
        options.append(
            ChoiceOption(
                text=otext,
                target=target,
                condition=cond,
                pos=Pos(oline.file, oline.lineno, oline.indent + 1),
            )
        )
        idx += 1
    if idx < n and lines[idx].indent > child_indent:
        raise _err(lines[idx], "BadIndent", "unexpected indent inside `choice`")
    if not options:
        raise _err(lines[idx], "EmptyChoice", "`choice` has no options")
    if not any(o.condition is None or _true_at_defaults(o.condition) for o in options):
        raise _err(
            lines[idx - len(options)],
            "UnreachableChoice",
            "no option in this `choice` is open when every flag is at its default; "
            "the menu could be empty",
        )
    return ChoiceStmt(options=tuple(options), pos=pos), idx


def _true_at_defaults(cond: Condition) -> bool:
    """Evaluate a condition as a fresh playthrough would: every flag unset,
    so it reads as false (and as 0 in an ordering comparison). Equality is
    type-strict, as in the player and the web runner."""
    value = False
    if cond.op == "truthy":
        return False
    if cond.op == "not":
        return True
    if cond.op == "==":
        return type(value) is type(cond.value) and value == cond.value
    if cond.op == "!=":
        return not (type(value) is type(cond.value) and value == cond.value)
    return {">=": 0 >= cond.value, "<=": 0 <= cond.value, ">": 0 > cond.value, "<": 0 < cond.value}[cond.op]


def _parse_if(lines: list[_Line], idx: int, indent: int, cond: Condition, pos: Pos):
    then_indent = _block_indent(lines, idx, indent)
    if then_indent is not None:
        then_stmts, idx = _parse_block(lines, idx, then_indent)
    else:
        then_stmts = []
    else_stmts: list = []
    if idx < len(lines) and lines[idx].indent == indent and lines[idx].text.strip() == "else":
        idx += 1
        else_indent = _block_indent(lines, idx, indent)
        if else_indent is not None:
            else_stmts, idx = _parse_block(lines, idx, else_indent)
    return IfStmt(condition=cond, then=tuple(then_stmts), else_=tuple(else_stmts), pos=pos), idx


def _parse_check(lines: list[_Line], idx: int, indent: int, stat: str, difficulty: int, pos: Pos):
    child_indent = _block_indent(lines, idx, indent)
    outcomes = {"style": None, "success": None, "tie": None, "fail": None}
    n = len(lines)
    if child_indent is not None:
        while idx < n and lines[idx].indent == child_indent:
            oline = lines[idx]
            m = OUTCOME_CHECK_RE.match(oline.text)
            if not m:
                raise _err(oline, "BadOutcome", f"malformed check outcome: {oline.text!r}")
            tier, target = m.groups()
            outcomes[tier] = target
            idx += 1
        if idx < n and lines[idx].indent > child_indent:
            raise _err(lines[idx], "BadIndent", "unexpected indent inside `check`")
    if not any(outcomes.values()):
        raise _err(lines[idx - 1] if idx > 0 else lines[idx], "EmptyCheck", "`check` has no outcomes")
    return CheckStmt(stat=stat, difficulty=difficulty, outcomes=outcomes, pos=pos), idx


def _parse_puzzle(lines: list[_Line], idx: int, indent: int, puzzle_id: str, pos: Pos):
    child_indent = _block_indent(lines, idx, indent)
    outcomes = {"pass": None, "lockout": None}
    n = len(lines)
    if child_indent is not None:
        while idx < n and lines[idx].indent == child_indent:
            oline = lines[idx]
            m = OUTCOME_PUZZLE_RE.match(oline.text)
            if not m:
                raise _err(oline, "BadOutcome", f"malformed puzzle outcome: {oline.text!r}")
            tier, target = m.groups()
            outcomes[tier] = target
            idx += 1
        if idx < n and lines[idx].indent > child_indent:
            raise _err(lines[idx], "BadIndent", "unexpected indent inside `puzzle`")
    if not outcomes["pass"]:
        raise _err(
            lines[idx - 1] if idx > 0 else lines[idx],
            "MissingPassOutcome",
            f"`puzzle {puzzle_id}` needs a `pass -> label` outcome",
        )
    return PuzzleStmt(puzzle_id=puzzle_id, outcomes=outcomes, pos=pos), idx
