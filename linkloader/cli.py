"""CLI entry point for linkloader.

    python -m linkloader check story/
    python -m linkloader export story/ -o build/story.json
    python -m linkloader play story/ [--seed N] [--script inputs.txt]
    python -m linkloader build story/ -o dist/
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

from .build import BuildError, build as run_build
from .errors import LinkLoaderError, ParseError, ValidationError
from .exporter import export_story
from .loader import load_cast_and_assets, load_story
from .player import Player, ScriptExhausted
from .validator import validate


def _load_and_validate(story_dir: Path, root: Path):
    """Returns (story, cast, assets, errors, warnings). Raises
    LinkLoaderError only for problems that stop us before validation
    can even run (a parse error, or a missing cast/assets file)."""
    story = load_story(story_dir)
    try:
        cast, assets = load_cast_and_assets(story_dir)
    except (FileNotFoundError, ValueError, tomllib.TOMLDecodeError) as e:
        # A missing or malformed cast.toml/assets.toml. Report it like a
        # parse error, not a traceback. Caught here only, so a ValueError
        # from a real bug elsewhere still shows its traceback.
        raise LinkLoaderError(f"error: {e}") from e
    puzzles_dir = root / "puzzles"
    errors, warnings = validate(story, cast, assets, puzzles_dir)
    return story, cast, assets, errors, warnings


def cmd_check(args: argparse.Namespace) -> int:
    story_dir = Path(args.story_dir)
    root = Path(args.root) if args.root else Path.cwd()
    try:
        story, cast, assets, errors, warnings = _load_and_validate(story_dir, root)
    except LinkLoaderError as e:
        print(str(e), file=sys.stderr)
        return 1

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(
        f"OK: {len(story.scenes)} scene(s) across {len(story.files)} file(s), "
        f"{len(warnings)} warning(s)"
    )
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    story_dir = Path(args.story_dir)
    root = Path(args.root) if args.root else Path.cwd()
    try:
        story, cast, assets, errors, warnings = _load_and_validate(story_dir, root)
    except LinkLoaderError as e:
        print(str(e), file=sys.stderr)
        return 1

    for w in warnings:
        print(f"warning: {w}")
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print("export refused: fix the errors above first", file=sys.stderr)
        return 1

    data = export_story(story, cast, assets)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


def cmd_play(args: argparse.Namespace) -> int:
    story_dir = Path(args.story_dir)
    root = Path(args.root) if args.root else Path.cwd()
    try:
        story, cast, assets, errors, warnings = _load_and_validate(story_dir, root)
    except LinkLoaderError as e:
        print(str(e), file=sys.stderr)
        return 1

    for w in warnings:
        print(f"warning: {w}")
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print("play refused: fix the errors above first", file=sys.stderr)
        return 1

    script = None
    if args.script:
        lines = Path(args.script).read_text(encoding="utf-8").splitlines()
        script = [line for line in lines if line.strip() != "" and not line.startswith("#")]

    stats = {"cosmonaut": args.cosmonaut, "cowboy": args.cowboy, "coder": args.coder}
    player = Player(
        story, cast, root, seed=args.seed, script=script, fate_points=args.fate, stats=stats
    )
    try:
        ending = player.run()
    except ScriptExhausted as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"\n[the story ends at scene: {ending}]")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    story_dir = Path(args.story_dir)
    root = Path(args.root) if args.root else Path.cwd()
    out_dir = Path(args.output)
    try:
        report = run_build(story_dir, out_dir, root)
    except (LinkLoaderError, BuildError) as e:
        print(str(e), file=sys.stderr)
        return 1

    for w in report["warnings"]:
        print(f"warning: {w}")
    print(
        f"OK: built {report['scenes']} scene(s), "
        f"{len(report['puzzle_ids'])} puzzle(s), "
        f"{report['assets_copied']} asset(s) -> {out_dir}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m linkloader")
    parser.add_argument(
        "--root",
        default=None,
        help="project root containing puzzles/ (default: current directory)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="parse and validate a story directory")
    p_check.add_argument("story_dir")
    p_check.set_defaults(func=cmd_check)

    p_export = sub.add_parser("export", help="export a story directory to JSON")
    p_export.add_argument("story_dir")
    p_export.add_argument("-o", "--output", required=True)
    p_export.set_defaults(func=cmd_export)

    p_play = sub.add_parser("play", help="play a story in the terminal")
    p_play.add_argument("story_dir")
    p_play.add_argument("--seed", type=int, default=None)
    p_play.add_argument("--script", default=None, help="file of newline-separated inputs")
    p_play.add_argument("--fate", type=int, default=3)
    p_play.add_argument("--cosmonaut", type=int, default=0)
    p_play.add_argument("--cowboy", type=int, default=0)
    p_play.add_argument("--coder", type=int, default=0)
    p_play.set_defaults(func=cmd_play)

    p_build = sub.add_parser("build", help="build the static web game into a dist/ folder")
    p_build.add_argument("story_dir")
    p_build.add_argument("-o", "--output", required=True)
    p_build.set_defaults(func=cmd_build)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ParseError, ValidationError) as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
