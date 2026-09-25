"""Validate a parsed Story against itself, `cast.toml`, and
`assets.toml`, and check which `puzzles/<id>/` directories exist.

`validate()` returns `(errors, warnings)`. It never raises — callers
decide what to do with a non-empty `errors` list (the CLI's `check`
and `export` commands exit 1; `play` refuses to start).
"""

from __future__ import annotations

from pathlib import Path

from .errors import ValidationError, ValidationWarning
from .model import (
    Bg,
    CheckStmt,
    ChoiceStmt,
    Hide,
    IfStmt,
    Jump,
    Line,
    PuzzleStmt,
    Show,
    Story,
)


def walk_statements(stmts):
    """Yield every statement, recursing into `if` branches (the only
    statement kind that nests a statement list)."""
    for s in stmts:
        yield s
        if isinstance(s, IfStmt):
            yield from walk_statements(s.then)
            yield from walk_statements(s.else_)


def _targets_of(stmt):
    """Yield (target_label, pos) for every jump this statement can make."""
    if isinstance(stmt, Jump):
        yield stmt.target, stmt.pos
    elif isinstance(stmt, ChoiceStmt):
        for opt in stmt.options:
            yield opt.target, opt.pos
    elif isinstance(stmt, CheckStmt):
        for target in stmt.outcomes.values():
            if target:
                yield target, stmt.pos
    elif isinstance(stmt, PuzzleStmt):
        for target in stmt.outcomes.values():
            if target:
                yield target, stmt.pos


def validate(story: Story, cast: dict, assets: dict, puzzles_dir: Path):
    errors: list[ValidationError] = []
    warnings: list[ValidationWarning] = []

    if story.start not in story.scenes:
        errors.append(
            ValidationError(
                "MissingStart",
                f"no scene named {story.start!r} (the story's entry point)",
            )
        )
        return errors, warnings

    bg_assets = assets.get("bg", {})
    sprite_assets = assets.get("sprite", {})

    # Per-scene, per-statement checks: bad jumps, unknown assets, unknown
    # speakers.
    for label, scene in story.scenes.items():
        for stmt in walk_statements(scene.statements):
            for target, pos in _targets_of(stmt):
                if target not in story.scenes:
                    errors.append(
                        ValidationError(
                            "BadJump",
                            f"{pos}: jump target {target!r} does not exist",
                            scene=label,
                        )
                    )
            if isinstance(stmt, Bg):
                if stmt.name not in bg_assets:
                    errors.append(
                        ValidationError(
                            "UnknownAsset",
                            f"{stmt.pos}: bg {stmt.name!r} is not in assets.toml [bg]",
                            scene=label,
                        )
                    )
            elif isinstance(stmt, Show):
                if stmt.sprite not in cast:
                    errors.append(
                        ValidationError(
                            "UnknownSpeaker",
                            f"{stmt.pos}: sprite {stmt.sprite!r} is not in cast.toml",
                            scene=label,
                        )
                    )
                sprite_table = sprite_assets.get(stmt.sprite, {})
                if stmt.expression not in sprite_table:
                    errors.append(
                        ValidationError(
                            "UnknownAsset",
                            f"{stmt.pos}: expression {stmt.expression!r} is not in "
                            f"assets.toml [sprite.{stmt.sprite}]",
                            scene=label,
                        )
                    )
            elif isinstance(stmt, Hide):
                if stmt.sprite not in cast:
                    errors.append(
                        ValidationError(
                            "UnknownSpeaker",
                            f"{stmt.pos}: sprite {stmt.sprite!r} is not in cast.toml",
                            scene=label,
                        )
                    )
            elif isinstance(stmt, Line):
                if stmt.speaker not in cast:
                    errors.append(
                        ValidationError(
                            "UnknownSpeaker",
                            f"{stmt.pos}: speaker {stmt.speaker!r} is not in cast.toml",
                            scene=label,
                        )
                    )
            elif isinstance(stmt, PuzzleStmt):
                if not (puzzles_dir / stmt.puzzle_id).is_dir():
                    warnings.append(
                        ValidationWarning(
                            "MissingPuzzleDir",
                            f"{stmt.pos}: no directory puzzles/{stmt.puzzle_id}/ yet "
                            "(puzzle content may land later)",
                            scene=label,
                        )
                    )

    # A check or puzzle that is the last statement of its scene and leaves
    # an outcome out ends the game when that outcome comes up (an absent
    # outcome falls through, and there is nothing to fall through to).
    for label, scene in story.scenes.items():
        if not scene.statements:
            continue
        last = scene.statements[-1]
        if isinstance(last, (CheckStmt, PuzzleStmt)):
            missing = [k for k, v in last.outcomes.items() if v is None]
            if missing:
                warnings.append(
                    ValidationWarning(
                        "OutcomeEndsGame",
                        f"{last.pos}: outcome(s) {', '.join(missing)} are missing and "
                        "nothing follows, so the game ends there",
                        scene=label,
                    )
                )

    # Reachability, from `start`, over every jump-capable statement.
    reachable = {story.start}
    frontier = [story.start]
    while frontier:
        label = frontier.pop()
        scene = story.scenes.get(label)
        if scene is None:
            continue
        for stmt in walk_statements(scene.statements):
            for target, _pos in _targets_of(stmt):
                if target in story.scenes and target not in reachable:
                    reachable.add(target)
                    frontier.append(target)

    for label in story.scenes:
        if label not in reachable:
            errors.append(
                ValidationError(
                    "UnreachableScene",
                    f"scene {label!r} cannot be reached from {story.start!r}",
                    scene=label,
                )
            )

    return errors, warnings
