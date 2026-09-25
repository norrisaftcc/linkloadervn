# Wave 2 plan

Status: approved. The owner accepted every default below.

## Decisions

1. `read-brand` and `rebalance-coupling` are optional puzzles. Neither blocks the story. `docs/canon/bible.md` changes in the same commit as the scenes that add them.
2. The room ships as described. The owner judges it in the built game before merge. The fallback in section 2 stays available.
3. The found document plays all 34 lines of `docs/canon/found-document.md`, verbatim, in file order.
4. The room art ships as an SVG now. A hand-drawn plate is a later art request.


## 1. Summary

1. Wave 2 adds three new Rill puzzles: `read-brand`, `count-herd` and `rebalance-coupling`. The spine then climbs from list access to recursion that filters, and then to recursion that builds a list.
2. The Clipi segment gets a phrasing `choice` before `count-crew`. The safe answer is "Say fen": Slim gives Clipi a word for an end point, which is the base case in words.
3. The found-document scene plays the log verbatim and in file order, in the inner stratum.
4. Yes, a small room can be Clipi's interface. It is a symptom of the reboot, it appears once, it has three objects and no helper character, and it uses the inner stratum.
5. The runner gets one new statement (`mode`) and CSS. It gets no new panel. `rill.js` and the checker do not change.

## 2. The room

**Decision.** The room is Clipi's interior during the reboot. It is not Clipi's everyday interface. Everywhere else, Clipi stays a voice in the normal dialogue box. The room appears in one scene group, between `found_document` and `confrontation`. The player walks into it once and leaves through its door.

**Look.** A flat CRT view of a bare room. The plate is `--color-paper-deep` with ink outlines, and the room is flat with no perspective. The page uses the brand's inner stratum: a halftone dot overlay, low scanlines and a heavier ink border on the dialogue box. There are three objects:

- **Chest of drawers.** This is a list: `hesh` is the top drawer and `tull` is the rest of the chest. Opening it starts `count-herd`.
- **Window.** This is `husk?` as flavor, with no puzzle. It shows a strip of desert if `clipi_stable` is true, and static if it is not. It proves that the room sits inside the same story.
- **Door.** This is the exit to `confrontation`. It appears only after the chest is done.

**How it stays original.** No character stands in the room. Clipi *is* the room and speaks only as a voice. The objects open beats (a puzzle, a line of narration, an exit), not programs. There is no icon grid, no desktop and no dog. The only magenta is flat fills on object outlines. All names and shapes are new.

**Fallback.** If the owner finds it too close to the reference, cut the `clipi_room` scenes and send `found_document` straight to `confrontation`. Then play `count-herd` from a plain `puzzle` statement in `found_document`'s place. The puzzles and the phrasing choice need no room.

## 3. Puzzles

| id | Title | Teaches | Where |
|---|---|---|---|
| `read-brand` | Read the rustler brand | Put `hesh` and `tull` together to reach one position | `02-sabotage.scene`, optional, before `git_blame` |
| `count-herd` | Count the herd | Recursion that filters and counts | `03b-room.scene`, the chest of drawers |
| `rebalance-coupling` | Rebalance the coupling | Recursion that builds a new chain with `bind` | `05-resolution.scene`, optional, before the ending choice |

`count-crew` and `find-signal` do not change. Both new optional puzzles send `pass` and `lockout` to the same next beat, so neither one can block the climax.

### read-brand

**Task.** Write `read-brand`, a `rig` of one chain, that returns the third word. The scene shows the brand as `(seal (kessa voth sil fen))`. The tests run on three different chains, so a hardcoded answer fails.

```scheme
(stake read-brand
  (rig (chain-in)
    (hesh (tull (tull chain-in)))))
```

**Wrong answers:**
- One `tull` short: `(hesh (tull chain-in))` returns `voth`.
- One `tull` too many: `(hesh (tull (tull (tull chain-in))))` returns `fen`.
- Wrong order: `(tull (hesh chain-in))` errors.
- Hardcoded: `(seal sil)` fails the tests on the other chains.

**Tests.** `(seal (kessa voth sil fen))` gives `sil`. `(seal (haan haan drev))` gives `drev`. `(seal (mora dray fen))` gives `fen`.

### count-herd

**Task.** There are two blanks: the word that marks a wreck, and what to recurse on when an entry is kept. `haan` is kin and `voth` is a planted wreck.

```scheme
(stake herd-count
  (rig (chest)
    (reckon (husk? chest)
            0
            (reckon (same? (hesh chest) (seal voth))
                    (herd-count (tull chest))
                    (sum 1 (herd-count (tull chest)))))))
```

**Wrong answers:**
- Branches swapped: this counts the wrecks.
- The `voth` test is dropped: this counts every entry.
- The test uses `haan` in place of `voth`: this inverts the filter.
- The keep branch recurses on `chest`: this never ends. chibi stops it with "out of stack space" and `rill.js` stops it with "ran too long".

**Tests.** `(chain)` gives 0. `(seal (voth))` gives 0. `(seal (haan voth haan))` gives 2. `(seal (voth haan voth haan haan))` gives 3.

### rebalance-coupling

**Task.** Walk the chain, drop every `voth`, and rebuild the rest in order. There are three blanks: the empty base case, what to `bind` onto the front, and what to recurse on.

```scheme
(stake rebalance
  (rig (links)
    (reckon (husk? links)
            (chain)
            (reckon (same? (hesh links) (seal voth))
                    (rebalance (tull links))
                    (bind (hesh links) (rebalance (tull links)))))))
```

**Wrong answers:**
- The base case is `(seal (voth))`: every result gets a trailing `voth`.
- Branches swapped: this keeps only the wrecks.
- It binds `(tull links)` in place of the head: the result is nested.
- It uses `chain` in place of `bind`: the result is nested.
- It recurses on `links`: this never ends.

**Tests.** `(chain)` gives `()`. `(seal (voth voth))` gives `()`. `(seal (kessa voth kessa))` gives `(kessa kessa)`. `(seal (voth sil voth fen))` gives `(sil fen)`.

**Checks run.** I ran every reference answer and wrong answer above through `web/rill/rill.js` `checkAnswer`. I also ran the reference answers through chibi-scheme with `prelude.scm` loaded. All reference answers passed and all wrong answers failed.

**Rill fixes carried from the judges:**
- The story-first tape literal `(bind kessa (bind voth ...))` does not appear anywhere. Scene data is always wrapped in `seal`.
- The improper-list `rebalance` (a chain ending in the symbol `voth`) is dropped. The chain now ends empty and the test is `husk?`.
- The `haan-census` helper, which had a naming mismatch, is dropped.
- The timeout risk was overstated. Endless recursion fails fast in both engines, so `RILL_TIMEOUT` does not change.
- The hardcoded-answer gap is closed for `read-brand`, because it is now a `rig` tested on several chains.

## 4. The Clipi segment and the found-document scene

### Clipi segment (`story/03-clipi.scene`)

1. `clipi_check` does not change. It keeps the kept lines and the `coder` check.
2. The three `talk_down_*` scenes now jump to a new scene, `clipi_phrase`. It opens with one Clipi line that has one more paren than the kept line: "I'm not in the (((loop)))." This line is new and is not marked as kept. Then a `choice`:
   - "Come back around, Clipi." jumps to `clipi_worse`.
   - "Say it again. Slower." jumps to `clipi_worse`.
   - "You're not going anywhere. Say fen." jumps to `clipi_settles`.
3. `clipi_worse` does `set spiral += 1`, shows `clipi glitch` and adds another paren. If `spiral >= 2`, one line of narration plays and the scene jumps to `clipi_puzzle`. If not, it jumps back to `clipi_phrase`.
4. `clipi_settles`: Clipi says "Fen." and the scene jumps to `clipi_puzzle`.
5. `clipi_puzzle` keeps `count-crew` as it is. Its blank is the base case that ends the loop.

This segment needs no runner changes. It uses `choice`, `set` and `if` as they exist today.

### Found-document scene (`found_document`)

1. The scene starts with `mode inner`.
2. Clipi reads every line of `found-document.md` as a `clipi:` line, verbatim and in file order. A scene comment above each line gives its `file:line`, as the rules require.
3. The jump from line 25 to line 49 plays with no bridge. The skip is Clipi's memory.
4. After line 84 ("Sorry, you're right. I'm not sure why I did that."), Slim asks: `Who's "Copilot"?` This line is from the placeholder and is not a kept line.
5. Clipi does not answer. It reads lines 87 to 130 and ends on the tail-recursion comment.
6. No narration is added and there is no puzzle. The scene then jumps to `clipi_room`.

### Room scenes (`story/03b-room.scene`)

1. `clipi_room` sets `mode inner` and `bg clipi_room` and hides all sprites. One line of narration plays: "The floor holds. A chest of drawers, a window, a door."
2. `room_hub` is a `choice`:
   - "Open the chest of drawers." jumps to `room_chest`, if `not herd_done`.
   - "Look out the window." jumps to `room_window`.
   - "Go through the door." jumps to `confrontation`, if `herd_done`.
3. `room_chest` plays `puzzle count-herd`. Both `pass` and `lockout` do `set herd_done = true`, play one Clipi line each, and return to the hub.
4. `room_window` uses `if clipi_stable` to show the desert or the static.

Every room scene starts with `mode inner`.

## 5. Runner and format changes

1. **New statement `mode <name>`.** It is one line at top level. `<name>` is `default` or `inner`. Any other value is a validator error, `UnknownMode`.
   - Add a `ModeStmt` to the model, the parser, the validator and the exporter. The export is `{"kind": "mode", "name": "inner"}`.
   - The terminal player ignores it.
2. **runner.js.** Add `case "mode":`, which sets `#game`'s `data-mode` attribute to the name. `gotoScene` resets `data-mode` to `default` on every scene entry. So `mode` lasts until the end of the scene, and a save made at scene entry always restores the right look. There is no new save field.
3. **stage.css.** Add `[data-mode="inner"]` rules, using existing tokens only:
   - A dot-halftone overlay on `.stage`, reusing the puzzle panel's dot grid at about 14 percent.
   - A low-opacity `repeating-linear-gradient` for scanlines.
   - A heavier `--color-ink` border on `.dialogue-box`.
   - `.choice-btn` drawn as flat labeled tiles.

   There are no new colors or fonts, and magenta stays a flat fill.
4. **docs/scene-format.md.** Add a `mode` section and its JSON shape. Change "eight statement families" to "nine".
5. **assets.toml.** Add one `[bg]` key, `clipi_room`, that points to `story/art/clipi_room.svg`.
6. **Puzzle cases.** Add three puzzle folders. Add their cases to `puzzles/check/gen_cases.scm`, which lists cases by hand. Then regenerate `puzzles/cases.json`.

There is no change to `rill.js`, `harness.scm`, `run.sh` or the `puzzle` statement.

## 6. Art

**CSS/SVG can do all of this today:**
- `clipi_room.svg`: a back wall, a floor line, a chest of drawers with three drawer lines, a round window and a door rectangle. It uses ink outlines on paper-deep, one idea per shape, and magenta only as flat outline fills.
- The halftone and scanline overlays, in pure CSS.
- The window's desert strip. It can reuse the `desert_night` image, clipped with CSS.

**Art requests for the owner (none of these block Wave 2):**
1. A hand-drawn duotone line-art plate of the room, to replace the SVG later. It must pass `despill.py --scan`.
2. Ambient motion (a flicker, a drawer that slides) or more than three objects. Scope this separately.
3. No new character art. Clipi has no sprite in the room.

## 7. Work breakdown

Each task is sized for one Sonnet agent.

**Wave A (runs in parallel):**

| Task | Owned paths | Acceptance |
|---|---|---|
| A1 `read-brand` puzzle | `puzzles/read-brand/` | `bash puzzles/check/run.sh read-brand puzzles/read-brand/answer.rill`; the full `bash puzzles/check/run.sh` passes |
| A2 `count-herd` puzzle | `puzzles/count-herd/` | Same, for `count-herd` |
| A3 `rebalance-coupling` puzzle | `puzzles/rebalance-coupling/` | Same, for `rebalance-coupling` |
| A4 `mode` in Python | `linkloader/{model,parser,validator,exporter,player}.py`, `docs/scene-format.md`, `tests/test_mode.py` | `pytest tests`; the tests cover parse, `UnknownMode` and the export shape |
| A5 `mode` in the web runner | `web/runner.js`, `web/stage.css` | `cd web/rill && node --test`; a unit test or e2e stub checks that `data-mode` resets on `gotoScene` |
| A6 Room SVG | `story/art/clipi_room.svg`, `story/assets.toml` | The SVG uses only token colors; review it by eye against `brand.md` |

Each puzzle folder in A1 to A3 holds `puzzle.md`, `starter.rill`, `answer.rill`, `tests.scm` and 3 or more files in `wrong/`.

**Wave B (depends on A):**

| Task | Owned paths | Depends on | Acceptance |
|---|---|---|---|
| B1 Cases | `puzzles/check/gen_cases.scm`, `puzzles/cases.json` | A1 to A3 | `chibi-scheme -q puzzles/check/gen_cases.scm > puzzles/cases.json`; `cd web/rill && node --test` |
| B2 Clipi segment and found document | `story/03-clipi.scene` | A4 | `python -m linkloader check story/`; `python -m linkloader play story/ --seed 1 --script <inputs>` reaches `clipi_room` |
| B3 Room | `story/03b-room.scene` | A2, A4, A6 | `python -m linkloader check story/`; `python -m linkloader build story/ -o dist/` |
| B4 Sabotage, resolution and bible | `story/02-sabotage.scene`, `story/05-resolution.scene`, `docs/canon/bible.md` | A1, A3 | `python -m linkloader check story/` |

**Wave C (depends on B):**

| Task | Owned paths | Acceptance |
|---|---|---|
| C1 End-to-end | `tests/e2e/test_web.py`, `web/guide/shots/` | All the checks in AGENTS.md pass; the Playwright test walks the room hub and sees `data-mode="inner"`; `python tools/guide/capture.py dist/ web/guide/shots/` |

## 8. Open questions for the owner

1. **The bible says scene 3 has no puzzle and that the game has three puzzles.** May `read-brand` and `rebalance-coupling` go in as optional puzzles that do not gate the story, with a one-line bible change? *Default: yes. B4 updates the spine in the same commit.*
2. **Is the room too close to the 1995 reference?** *Default: ship it as written (three objects, voice only, inner stratum). Look at the built page before merge. If it is too close, use the fallback in section 2.*
3. **Should the found document play all 34 lines, or a trimmed set?** *Default: all lines in file order. Nothing is trimmed, so there is no decision about which lines to cut.*
4. **Should the room SVG ship now, or wait for a hand-drawn plate?** *Default: ship the SVG now and log the plate as art request 1.*