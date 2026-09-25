# Cut: What's Not Coming Back, and Why

## Neon Taxidermy

`docs/neon_taxidermy_design.md` describes a different game entirely: a
cyberpunk crafting narrative about "digital preservation artisans" who
embalm dying AIs and uploaded minds in glowing display cases, built
around three stats (Technique, Empathy, Innovation) and a five-stage
decay/preservation loop. It shares no character, no location, and no
mechanic with Link Loader — it reads as an unrelated pitch that landed
in this repo's `docs/` folder.

**Cut entirely.** It doesn't extend the Debug Western; it competes with
it. If any piece of it is wanted later (the decay-state idea is not
bad), it should be spun out as its own project, not folded into
Syntax-4.

## Constellation Engine

`docs/constellation_kanban.md` and `src/constellation/README.md`
describe a from-scratch, browser-native visual novel engine ("web-native
visual novel engine for LinkLoader"): its own JSON story format, its own
CSS theming system, its own JavaScript renderer with a typewriter effect
and choice/branching UI, planned save/load via `localStorage`, and a
planned "minigame framework." A kanban board tracks its sprints.

This predates the owner's decision recorded in this task: **the build
is Python plus plain-text scene files**, emitting a static web export
and a terminal player, with Flask+SQLite as a possible later addition
for logging puzzle attempts. A second, parallel JS engine is now a
duplicate effort — different language, different story format,
different renderer, no shared code path to the chosen build.

**Cut as an active codepath.** `src/constellation/` and the two docs
should not be extended or wired into the Python build. They can stay in
the repo as historical record of an earlier direction, but nothing in
the new pipeline should import, generate for, or otherwise depend on
Constellation. If its CSS theming ideas are useful for the static web
export's look, that's a design reference only, not a code dependency.

## Orphan labels in the old Ren'Py scripts

One clear case, verified by reading the control flow directly (not
part of `kept.md`/`found-document.md`'s quote-verification scope,
since this is a structural claim about the script rather than a quoted
line), and one claim from an earlier draft of this document that did
not hold up and has been removed:

- The alpha scripts at commit `79da7b8` each
  define a dead `game`/`scene2` pair. In
  `renpy/alphas/link_loader_1_1/game/script.rpy`, `label start:` ends
  in a `return` at line 219; `label game:` begins at line 225, after
  that `return`, and nothing in the file ever `jump`s or `call`s to
  `game` — it is unreachable. `label scene2:` immediately follows at
  line 244 with no intervening `jump`, so it too is only reached if
  `game` is ever entered, which it isn't. The same pair appears at
  lines 215/221/240 in the sibling alpha,
  `renpy/alphas/ll_alpha0.2/game/script.rpy`.
- Correction: an earlier draft of this cut list claimed the same
  orphan pair also appears in `examples/renpy/script.rpy`. On
  re-checking the control flow, that file has no `label game:` at all —
  every label (`start`, `scene1`, `scene2`, the three `scene3_*`
  approaches, `scene4`, `scene5`) is reached by an explicit `jump`, and
  the file's single `return` sits at the end of `scene5`, the last
  label. `examples/renpy/script.rpy` has no orphan labels; that earlier
  claim was wrong and is retracted here.

**Cut.** The new spine (`bible.md`) has one label per scene and no
scene that outlives its own `return`/jump. Nothing here was a joke
worth keeping — it's leftover scaffolding from an early two-scene demo
structure that the script outgrew without deleting.

## The "COS/COW/COD via git blame" mini-game promises

The design doc (`docs/script.md`) and the two working alphas each
promise a *different* mini-game per approach in Scene 3 — a timed
syntax-race for Cosmonaut, a physical tamper-hunt for Cowboy, a
message-decoding puzzle for Coder — and none of them were ever built;
every approach branch just prints a line and jumps straight to Scene 4.

**Cut as three separate systems.** Building three different minigame
engines for one branch each does not fit a small, testable revival.
The new spine instead gives every approach the *same* Rill puzzle
mechanic (a Scheme s-expression checked by chibi-scheme) with
flavor text that reflects which approach the player is using. The
promise of "your approach changes how the puzzle looks" survives; the
promise of "three different mini-game engines" does not.

## Sh- dialect as color only, not as a second puzzle language

The old scripts sometimes use the cargo bots' `(Sh-word word word)`
speech as flavor text and sometimes seem to gesture at it as something
the player parses (Scene 2's branch where low Coder means Clipi has to
"translate"). We are not building two conlang puzzle systems.

**Cut the idea of Sh- as a solvable code.** Rill (the s-expression
conlang, owned by a separate lexicon — see "Rill, briefly" in
`bible.md` for its location) is the one puzzle language. The cargo
bots' "Sh-" speech stays
exactly what it already was in the kept lines: a spoken-parentheses
accent flavoring dialogue, not a second thing for the player to decode.

## Multiple near-duplicate scripts as separate canon

`docs/script.md` (a prose novelization of the "Clipi" script),
`examples/renpy/script.rpy` (a cleaned near-duplicate of the current
game script, sharing labels like `scene1`/`scene2` instead of the
current `scene1_intro`/`scene2_link_loader`), and
`renpy/current/script.rpy_bak.rpy` (a 374-line partial draft, same era,
same characters, incomplete) are all drafts of the same story beat as
the current 655-line `script.rpy`.

**Cut as separate canon.** They're read as sources for `kept.md` and
this document but none of them is a distinct scene or a distinct
draft worth preserving as-is; the current, longest, most complete
script (`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy`)
is the reference text going forward.
