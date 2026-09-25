"""The `.scene` AST: one dataclass per statement kind.

Every statement carries a `pos` (file, line, column) so the validator
can report exactly where a bad jump or unknown asset came from, even
though parsing already finished.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pos:
    file: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.col}"


# ---------------------------------------------------------------------------
# Conditions and assignments (shared by `set`, `if`, and `choice ... if`).

TRUTHY = "truthy"
NOT = "not"
COMPARE_OPS = ("==", "!=", ">=", "<=", ">", "<")


@dataclass(frozen=True)
class Condition:
    flag: str
    op: str  # "truthy" | "not" | one of COMPARE_OPS
    value: object = None  # bool | int | None


@dataclass(frozen=True)
class Assignment:
    flag: str
    op: str  # "=" | "+=" | "-="
    value: object  # bool | int


# ---------------------------------------------------------------------------
# Statements.


@dataclass(frozen=True)
class Bg:
    name: str
    pos: Pos


@dataclass(frozen=True)
class Show:
    sprite: str
    expression: str
    position: str  # "left" | "center" | "right"
    pos: Pos


@dataclass(frozen=True)
class Hide:
    sprite: str
    pos: Pos


@dataclass(frozen=True)
class Line:
    speaker: str
    text: str
    pos: Pos


@dataclass(frozen=True)
class Narration:
    text: str
    pos: Pos


@dataclass(frozen=True)
class SetStmt:
    assignments: tuple[Assignment, ...]
    pos: Pos


@dataclass(frozen=True)
class IfStmt:
    condition: Condition
    then: tuple["Statement", ...]
    else_: tuple["Statement", ...]
    pos: Pos


@dataclass(frozen=True)
class ChoiceOption:
    text: str
    target: str
    condition: Condition | None
    pos: Pos


@dataclass(frozen=True)
class ChoiceStmt:
    options: tuple[ChoiceOption, ...]
    pos: Pos


@dataclass(frozen=True)
class CheckStmt:
    stat: str  # "cosmonaut" | "cowboy" | "coder"
    difficulty: int
    outcomes: dict  # {"style": str|None, "success": str|None, "tie": str|None, "fail": str|None}
    pos: Pos


@dataclass(frozen=True)
class PuzzleStmt:
    puzzle_id: str
    outcomes: dict  # {"pass": str, "lockout": str|None}
    pos: Pos


@dataclass(frozen=True)
class Jump:
    target: str
    pos: Pos


Statement = (
    Bg
    | Show
    | Hide
    | Line
    | Narration
    | SetStmt
    | IfStmt
    | ChoiceStmt
    | CheckStmt
    | PuzzleStmt
    | Jump
)


@dataclass
class Scene:
    label: str
    statements: list = field(default_factory=list)
    pos: Pos = None


@dataclass
class Story:
    scenes: dict  # label -> Scene
    start: str = "start"
    files: list = field(default_factory=list)
