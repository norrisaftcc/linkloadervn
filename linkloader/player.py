"""The terminal player: walks a Story, printing scenes and taking
input for choices, checks, and puzzles.

`--script inputs.txt` feeds queued answers instead of reading stdin,
for non-interactive tests and demos. Puzzle answers are checked by
shelling out to `puzzles/check/run.sh` (see docs/scene-format.md).
"""

from __future__ import annotations

import random
import subprocess
from collections import deque
from pathlib import Path

from .dice import check as roll_check
from .model import (
    Bg,
    CheckStmt,
    ChoiceStmt,
    Condition,
    Hide,
    IfStmt,
    Jump,
    Line,
    ModeStmt,
    Narration,
    PuzzleStmt,
    SetStmt,
    Show,
    Story,
)


class ScriptExhausted(RuntimeError):
    """The player needed input but --script ran out of lines."""


class Player:
    def __init__(
        self,
        story: Story,
        cast: dict,
        root: Path,
        seed: int | None = None,
        script: list[str] | None = None,
        fate_points: int = 3,
        stats: dict | None = None,
        out=print,
    ):
        """`stats`, if given, seeds the initial flags (e.g. from the
        CLI's --cosmonaut/--cowboy/--coder). A `check`'s stat value is
        read from the flag of the same name at roll time (see
        `_stat_value`), so a scene's own `set` (e.g. the origin choice
        in story/01-arrival.scene) overrides whatever `stats` seeded."""
        self.story = story
        self.cast = cast
        self.root = Path(root)
        self.rng = random.Random(seed)
        self.script = deque(script) if script is not None else None
        self.fate = fate_points
        self.flags: dict = dict(stats) if stats else {}
        self.out = out

    # -- input -------------------------------------------------------

    def _input(self, prompt: str) -> str:
        if self.script is not None:
            if not self.script:
                raise ScriptExhausted(f"script ran out of input at prompt: {prompt!r}")
            answer = self.script.popleft()
        else:
            answer = input(prompt)
        return answer.strip()

    # -- flags and conditions ----------------------------------------

    def _get_flag(self, name: str):
        return self.flags.get(name, False)

    def _eval_condition(self, cond: Condition) -> bool:
        value = self._get_flag(cond.flag)
        if cond.op == "truthy":
            return bool(value)
        if cond.op == "not":
            return not value
        other = cond.value
        # Type-strict, like === in the web runner: true is not 1.
        same = type(value) is type(other) and value == other
        if cond.op == "==":
            return same
        if cond.op == "!=":
            return not same
        # >=, <=, >, < all need an int on the left; unset flags default to 0
        # for numeric comparisons, since they default to False (falsy).
        left = value if isinstance(value, int) and not isinstance(value, bool) else 0
        if cond.op == ">=":
            return left >= other
        if cond.op == "<=":
            return left <= other
        if cond.op == ">":
            return left > other
        if cond.op == "<":
            return left < other
        raise ValueError(f"unknown condition op: {cond.op!r}")

    def _apply_assignment(self, a) -> None:
        if a.op == "=":
            self.flags[a.flag] = a.value
            return
        current = self.flags.get(a.flag, 0)
        current = current if isinstance(current, int) and not isinstance(current, bool) else 0
        if a.op == "+=":
            self.flags[a.flag] = current + a.value
        elif a.op == "-=":
            self.flags[a.flag] = current - a.value

    # -- run -----------------------------------------------------------

    def run(self, start: str | None = None) -> str:
        """Play from `start` (default: the story's start scene) until a
        terminal scene is reached. Returns that scene's label."""
        label = start or self.story.start
        while True:
            scene = self.story.scenes[label]
            self.out(f"\n== {label} ==")
            result = self._run_statements(scene.statements)
            if result is None:
                return label
            label = result

    def _run_statements(self, stmts) -> str | None:
        i = 0
        n = len(stmts)
        while i < n:
            stmt = stmts[i]
            i += 1

            if isinstance(stmt, Bg):
                self.out(f"[bg: {stmt.name}]")
            elif isinstance(stmt, Show):
                self.out(f"[show {stmt.sprite} {stmt.expression} {stmt.position}]")
            elif isinstance(stmt, Hide):
                self.out(f"[hide {stmt.sprite}]")
            elif isinstance(stmt, Line):
                display = self.cast.get(stmt.speaker, {}).get("name", stmt.speaker)
                self.out(f"{display}: {stmt.text}")
            elif isinstance(stmt, Narration):
                self.out(f"> {stmt.text}")
            elif isinstance(stmt, SetStmt):
                for a in stmt.assignments:
                    self._apply_assignment(a)
            elif isinstance(stmt, IfStmt):
                branch = stmt.then if self._eval_condition(stmt.condition) else stmt.else_
                target = self._run_statements(branch)
                if target is not None:
                    return target
            elif isinstance(stmt, ChoiceStmt):
                target = self._do_choice(stmt)
                if target is not None:
                    return target
            elif isinstance(stmt, CheckStmt):
                target = self._do_check(stmt)
                if target is not None:
                    return target
            elif isinstance(stmt, PuzzleStmt):
                target = self._do_puzzle(stmt)
                if target is not None:
                    return target
            elif isinstance(stmt, Jump):
                return stmt.target
            elif isinstance(stmt, ModeStmt):
                pass  # the terminal player has no visual mode; ignored on purpose
            else:
                raise TypeError(f"unknown statement: {type(stmt)!r}")
        return None

    # -- individual block statements ----------------------------------

    def _do_choice(self, stmt: ChoiceStmt) -> str | None:
        options = [
            o for o in stmt.options if o.condition is None or self._eval_condition(o.condition)
        ]
        if not options:
            # Guarded UnreachableChoice should catch this at validation
            # time; this is a last-resort fallback so play never crashes.
            self.out("[no choices available]")
            return None
        for n, o in enumerate(options, start=1):
            self.out(f"  {n}. {o.text}")
        while True:
            answer = self._input("> ")
            try:
                n = int(answer)
                if 1 <= n <= len(options):
                    return options[n - 1].target
            except ValueError:
                pass
            self.out(f"[enter a number from 1 to {len(options)}]")

    def _stat_value(self, stat: str) -> int:
        """A check's stat value is the story flag with the same name
        as the stat (cosmonaut, cowboy, coder) if it holds an integer,
        else 0. See docs/scene-format.md, "check", and the matching
        rule in web/runner.js's renderCheck."""
        value = self.flags.get(stat, 0)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        return 0

    def _do_check(self, stmt: CheckStmt) -> str | None:
        stat_value = self._stat_value(stmt.stat)
        result = roll_check(stat_value, stmt.difficulty, self.rng)
        self.out(
            f"[check {stmt.stat}+{stat_value} vs {stmt.difficulty}: "
            f"dice={result.dice} total={result.total} -> {result.tier}]"
        )
        if self.fate > 0:
            answer = self._input("Spend a Fate point to reroll? [y/N] ")
            if answer.lower().startswith("y"):
                self.fate -= 1
                result = roll_check(stat_value, stmt.difficulty, self.rng)
                self.out(
                    f"[reroll: dice={result.dice} total={result.total} -> {result.tier}] "
                    f"(fate remaining: {self.fate})"
                )
        return stmt.outcomes.get(result.tier)

    def _do_puzzle(self, stmt: PuzzleStmt) -> str | None:
        run_sh = self.root / "puzzles" / "check" / "run.sh"
        puzzle_dir = self.root / "puzzles" / stmt.puzzle_id
        if not run_sh.exists() or not puzzle_dir.is_dir():
            self.out(
                f"[notice] no puzzle checker for '{stmt.puzzle_id}' yet; skipping puzzle."
            )
            return stmt.outcomes.get("lockout")

        self.out(f"[puzzle {stmt.puzzle_id}] see puzzles/{stmt.puzzle_id}/puzzle.md")
        while True:
            answer = self._input(
                f"puzzle {stmt.puzzle_id}> answer file path, 'hint', or 'skip': "
            )
            if answer == "skip":
                return stmt.outcomes.get("lockout")
            if answer == "hint":
                if self.fate > 0:
                    self.fate -= 1
                    self.out(
                        f"[hint] read puzzles/{stmt.puzzle_id}/puzzle.md and "
                        f"puzzles/rill/lexicon.md. (fate remaining: {self.fate})"
                    )
                else:
                    self.out("[no Fate points left]")
                continue

            answer_path = Path(answer)
            if not answer_path.is_absolute():
                answer_path = (Path.cwd() / answer_path).resolve()
            try:
                result = subprocess.run(
                    ["bash", str(run_sh), stmt.puzzle_id, str(answer_path)],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                )
            except FileNotFoundError:
                self.out("[notice] bash not found; skipping puzzle.")
                return stmt.outcomes.get("lockout")
            if result.stdout:
                self.out(result.stdout.rstrip())
            if result.returncode == 0:
                self.out(f"[puzzle {stmt.puzzle_id}: PASS]")
                return stmt.outcomes.get("pass")
            if result.stderr:
                self.out(result.stderr.rstrip())
            self.out(f"[puzzle {stmt.puzzle_id}: not solved]")
            return stmt.outcomes.get("lockout")
