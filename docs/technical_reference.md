# Technical Reference

How the pieces of the revived build fit together. The rules for working in
the repository, and the checks to run before a commit, are in `AGENTS.md`.

## Pipeline

1. `story/*.scene` hold the story, in the format described in
   `docs/scene-format.md`. `story/cast.toml` names the speakers and
   `story/assets.toml` maps backgrounds and sprites to image files.
2. `linkloader/parser.py` reads the scene files. `linkloader/validator.py`
   checks that every jump resolves, every scene is reachable, every asset
   and speaker exists, and no check or puzzle ends the game by accident.
3. `linkloader/exporter.py` turns the story into JSON.
   `linkloader/build.py` adds the dice ladder, the puzzles and the lexicon,
   copies the art the story uses, and writes `dist/` in one step: a failed
   build leaves the old `dist/` as it was.
4. `web/runner.js` plays `dist/story.json` in the browser.
   `linkloader/player.py` plays the same story in a terminal.

## Puzzles

- Rill is defined in `puzzles/rill/prelude.scm`. Its lexicon is
  `puzzles/rill/lexicon.md`.
- Each puzzle folder holds `puzzle.md` (player text, `## Hint` and
  `## Terminal`), `starter.rill`, `answer.rill`, `tests.scm` and `wrong/`.
- `puzzles/check/run.sh` checks answers under chibi-scheme. It rejects any
  form outside the Rill subset and stops each check after `RILL_TIMEOUT`
  seconds (default 5).
- `web/rill/rill.js` checks answers in the browser. Its tests replay
  `puzzles/cases.json` and compare every answer with chibi-scheme.

## Stats and checks

The three stats are cosmonaut, cowboy and coder. A check rolls 4dF, adds the
story flag with the stat's name, and reads the result against the
difficulty on the four-step ladder from High Tech, Low Lives: style,
success, tie, fail. A Fate point rerolls a check once or buys a puzzle hint.

## Tests

```bash
pytest tests                      # includes the Playwright end-to-end tests
bash puzzles/check/run.sh         # every puzzle under chibi-scheme
cd web/rill && node --test        # Rill in JavaScript, with chibi parity
```

## Legacy

- `renpy/current/` holds the original Ren'Py game. The committed SDK has no
  Python standard library, so it does not run from this repository.
- `src/tools/` holds the old Ren'Py-to-Twee and Ren'Py-to-JSON converters.
  Only `renpy_to_twee_v2.py` and `renpy_to_json.py` still run.
- The alphas and old HTML builds are in git history at commit `79da7b8`.
