# AGENTS.md

Instructions for coding agents (Claude Code, Codex, Copilot and others) in this repository.
`CLAUDE.md` imports this file. Edit this file, not `CLAUDE.md`.

## What this is

LinkLoader is a sci-fi western visual novel with code puzzles. Slim, a cowboy-cosmonaut-coder
on a desert moon, repairs link loaders: machines written in LISP. The puzzles use Rill, a
conlang that is Scheme with cowboy keywords. chibi-scheme checks every answer.

Audience: students, and volunteer testers from game dev, graphic design and programming.

## Layout

| Path | Contents |
|---|---|
| `linkloader/` | Python core: parser, validator, 4dF dice, JSON exporter, terminal player |
| `story/` | Scene files (`*.scene`), `cast.toml`, `assets.toml` |
| `puzzles/` | Rill prelude and lexicon, one folder per puzzle, the chibi harness |
| `tools/assets/` | Asset tools. `despill.py` removes the magenta chroma-key halo |
| `tests/` | pytest suite |
| `docs/scene-format.md` | The scene format spec |
| `docs/canon/` | Story bible, kept lines, found-document source, cut list |
| `docs/style/` | Brand guide, writing guide, `tokens.css`, specimen page |
| `web/` | The static web runner (`index.html`, `runner.js`, `stage.css`) and `web/rill/` (the JS Rill evaluator, contract C1 in its own files) |
| `web/guide/` | The shareable style guide page. The build copies it to `dist/guide/`. Refresh its screenshots with `python tools/guide/capture.py dist/ web/guide/shots/` |
| `dist/` | Output of `python -m linkloader build`: the playable one-folder web game. Generated, not committed |
| `renpy/current/.../link_loader_1_2/game/` | The old Ren'Py game. Source material only, and a later port target |

The old alphas and HTML builds are in history at commit `79da7b8`.

## Set up

1. Install chibi-scheme: `sudo apt-get install chibi-scheme`.
2. Make a virtual environment and install the dev dependencies: `pip install -e '.[dev]'`.

## Check your work

Run every command below before you commit. All must pass.

```bash
pytest tests
bash puzzles/check/run.sh
python -m linkloader check story/
python tools/assets/despill.py --scan renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/images
python -m linkloader build story/ -o dist/
cd web/rill && node --test
```

`pytest tests` already includes `tests/e2e/test_web.py`, the Playwright suite against a built
`dist/`. It skips itself cleanly if Playwright or a Chromium build is missing.

Run `node --test` from inside `web/rill/` (or pass it explicit files, `node --test
web/rill/*.test.mjs`). Passing `web/rill/` as a bare path to `node --test` from the repo root
does not recurse into it on every Node build; the two forms above do.

Other commands:

```bash
python -m linkloader play story/ [--seed N] [--script inputs.txt]
python -m linkloader export story/ -o build/story.json
bash puzzles/check/run.sh <puzzle-id> <answer-file>
```

## Rules

- The source of truth is the scene files and `puzzles/`. Web and terminal builds are outputs.
  Do not edit an output by hand.
- Do not edit the Ren'Py game to add features. It is source material. Fixes to its art are
  allowed.
- Rill is a strict subset of Scheme. The supported forms are listed at the top of
  `puzzles/rill/prelude.scm`. Do not add a form without adding cases to `puzzles/cases.json`.
  The JS and Python evaluators must give the same result as chibi on every case.
- Regenerate `puzzles/cases.json` with `chibi-scheme -q puzzles/check/gen_cases.scm`. Do not
  edit it by hand.
- Every puzzle needs a reference answer that passes and at least three wrong answers that fail.
- A new sprite must pass `despill.py --scan` before it goes in the game.
- Magenta is a flat fill. Never use it as a glow, shadow or edge.
- Keep story facts consistent with `docs/canon/bible.md`. If a scene must break the bible,
  change the bible in the same commit.
- Quotes from the old scripts stay verbatim, with `file:line`.

## Writing

Follow `docs/style/writing.md`. In short:

- Docs, UI text, puzzle prompts, commits and PRs: Simplified Technical English and Orwell's
  six rules. One instruction per sentence. Active voice. Use the same word for the same thing.
- Narrative prose: Gene Wolfe and Jack Vance as touchstones. Precise detail; do not explain
  the world to the reader.

## Git

- Work on a branch. Open a pull request to `main`.
- Keep each commit to one concern. Say what changed and why.
