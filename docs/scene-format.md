# The `.scene` format

A `.scene` file is plain text. It describes one or more scenes for
Link Loader. This document is the spec: the grammar, every statement,
every error the parser and validator can raise, and one full example.

Audience note: this spec assumes no background beyond reading Python
tracebacks. Terms are defined once, then used plainly.

## Files and encoding

- A story is a directory of `.scene` files, read in sorted filename
  order.
- Each file is UTF-8 plain text.
- A blank line is ignored.
- A line whose first non-space character is `#` is a comment and is
  ignored.
- Every other line is one **statement**.

## Lines, indentation, and blocks

Statements live at one of two levels:

- **Top level** — column 0. A scene header, or one of the one-line
  statements below.
- **Block body** — indented under a statement that opens a block
  (`choice`, `if`, `check`, `puzzle`). Indentation is spaces only (no
  tabs); the parser records the indent width of the first line of a
  block and requires every sibling line in that block to share it
  exactly. A line indented less than the block's width closes the
  block. A line indented *more* than the block's width, without
  opening a nested block itself, is a `BadIndent` error.

Blocks nest. An `if` block's `then` and `else` arms may themselves
contain any statement, including another `choice`, `check`, `if`, or
`puzzle`.

## Identifiers

A **label** (scene name, jump target) and a **flag** name are both
`[a-z][a-z0-9_]*`. Scene labels are unique across the whole story
(across all files).

## The start scene

The story's entry point is the scene labeled `start`. Every story
must define exactly one scene named `start`, and the validator's
reachability check walks from it.

## Statement reference

### Scene header

```
== <label>
```

Begins a new scene. Everything until the next `==` (or end of file)
belongs to this scene. A label may only be defined once in the whole
story.

**Errors**: `DuplicateLabel` (label already used in this story).

### `bg` — background

```
bg <name>
```

Sets the current background to `<name>`. `<name>` must be a key under
`[bg]` in `assets.toml`.

**Errors**: `UnknownAsset` — from the validator, not the parser, since
it needs `assets.toml` loaded. The parser accepts any identifier here.

### `show` / `hide` — sprites

```
show <sprite> <expression> [<position>]
hide <sprite>
```

`<position>` is one of `left`, `center`, `right`; it defaults to
`center` when omitted. `<sprite>` must be a key in `cast.toml`.
`<expression>` must be a key under `[sprite.<sprite>]` in
`assets.toml`.

**Errors**: `UnknownSpeaker` (sprite not in cast), `UnknownAsset`
(expression not mapped) — both from the validator.

### Dialogue

```
<speaker>: <text>
```

`<speaker>` is a bare identifier immediately followed by `:` and a
space, then free text running to the end of the line. `<speaker>`
must be a key in `cast.toml`.

**Errors**: `UnknownSpeaker` (validator).

### Narration

```
> <text>
```

A line of narration with no speaker. Text runs to the end of the
line.

### `choice` — a branch menu

```
choice
    "<text>" -> <label>
    "<text>" -> <label> [if <condition>]
```

Each indented line is one option: quoted display text, `->`, a jump
target, and an optional `if <condition>` guard (same condition syntax
as `if`, below). An option whose guard is false is not offered to the
player. A `choice` needs at least one option, and needs at least one
option reachable when all flags are at their default (so the menu can
never be empty on a fresh playthrough).

**Errors**: `EmptyChoice` (no options), `UnreachableChoice` (every
option is guarded, so the menu could be empty), `BadJump` (validator:
target label does not exist).

### `set` — assign flags

```
set <flag> = <value>
set <flag> += <n>
set <flag> -= <n>
set <flag> = <value>, <flag> = <value>, ...
```

`<value>` is `true`, `false`, or an integer literal. `+=`/`-=` require
an integer flag and an integer `<n>`; they create the flag at `0`
first if it is unset. Multiple assignments on one line are separated
by commas. Flags default to `false` (falsy) until first assigned, so
they don't need to be declared.

**Errors**: `BadValue` (parser: value is not `true`, `false`, or an
integer).

### `if` / `else` — a flag branch

```
if <condition>
    <statements>
else
    <statements>
```

`else` is optional. `<condition>` is one of:

```
<flag>                a truthy check (true, or a nonzero integer)
not <flag>
<flag> == <value>
<flag> != <value>
<flag> >= <n>
<flag> <= <n>
<flag> > <n>
<flag> < <n>
```

`<value>` is `true`, `false`, or an integer, matching `set`.

**Errors**: `BadCondition` (parser: malformed condition).

### `check` — a 4dF roll

```
check <stat> vs <difficulty>
    style -> <label>
    success -> <label>
    tie -> <label>
    fail -> <label>
```

`<stat>` is one of `cosmonaut`, `cowboy`, `coder` (see "Stats and the
ladder," below). `<difficulty>` is a non-negative integer, normally
one of `0`, `2`, `4`, `6` (the four named tiers), though the parser
accepts any non-negative integer.

Every outcome line is optional. An outcome that is present jumps to
its label. An outcome that is **absent** falls through: play
continues with the statement right after the `check` block, as if the
check had not branched at all. At least one outcome line must be
present — a `check` with every outcome absent has nothing that could
ever fire, so the parser rejects it as `EmptyCheck` regardless of what
follows the block.

A player may spend one Fate point to reroll a `check` once it lands.

**Errors**: `UnknownStat` (parser), `EmptyCheck` (parser), `BadJump`
(validator).

### `puzzle` — a Rill puzzle

```
puzzle <id>
    pass -> <label>
    lockout -> <label>
```

`<id>` names a directory under `puzzles/<id>/`, owned and populated by
a different part of the project. `pass` fires when
`puzzles/check/run.sh <id> <answer-file>` exits 0. `lockout` is
optional; when a player fails and no `lockout` outcome is given, play
falls through to the statement after the block (the puzzle is treated
as skippable, not a dead end). `pass` is required — a puzzle with no
way to succeed is a parser error.

A player may spend one Fate point to buy a hint instead of an
attempt (see the terminal player, below); this does not consume a
puzzle attempt.

If `puzzles/<id>/` does not exist on disk, the validator **warns**
(does not error) — puzzle content is built in parallel and may land
after this scene is written.

**Errors**: `MissingPassOutcome` (parser), `BadJump` (validator,
`lockout`/`pass` target). Missing puzzle directory is a **warning**,
not an error.

### `->` — jump

```
-> <label>
```

An unconditional jump to another scene. A scene that ends without a
final `choice`, `check`, `puzzle`, or `->` is a **terminal scene** —
the game ends there. This is intentional (it's how an ending is
written), not an error.

**Errors**: `BadJump` (validator: target label does not exist).

## Statement count

The format has eight statement families: scene headers, `bg`,
`show`/`hide`, dialogue/narration, `choice`, `set`/`if`, `check`, and
`puzzle`/`->` (jumps). That's the whole grammar.

## Stats and the ladder

Three stats, each rated `+0` to `+3` for a given player character
(the demo and any future character sheet own that rating; the engine
just reads it): `cosmonaut`, `cowboy`, `coder`.

A check rolls 4dF (four Fate dice, each `-1`/`0`/`+1`) plus the stat,
and compares the total against `<difficulty>` on the four-tier ladder
from *High Tech, Low Lives* (`/home/user/game-high-tech-low-lives/arcade/cabinet/SCENE-FORMAT.md`).
Only the rule is borrowed here, not any code from that project:

| Tier    | Condition                  |
|---------|-----------------------------|
| style   | `total >= difficulty + 3`  |
| success | `total >= difficulty + 1`  |
| tie     | `total == difficulty`      |
| fail    | anything else               |

Named difficulty tiers, for scene authors: Routine `0`, Challenging
`2`, Very difficult `4`, Nearly impossible `6`.

## Fate points

The player starts each session with a small pool of Fate points (the
terminal player defaults to `3`; a future character sheet may set
this). A Fate point may be spent:

- to **reroll** a `check` once, immediately after seeing its result;
- or to **buy a hint** on a `puzzle`, instead of attempting it.

Spending Fate points and gaining them back (e.g. from a `compel`) is
out of scope for this engine version — no scene statement grants Fate
points yet. That's an open issue, not an oversight; see the final
report for this task.

## Errors

Every error is one of two kinds:

- **Parse errors** — raised while reading a `.scene` file, before any
  cross-file checks. Each carries a file path, line number, and
  column. Examples: `BadIndent`, `BadValue`, `BadCondition`,
  `UnknownStat`, `EmptyCheck`, `EmptyChoice`, `MissingPassOutcome`,
  `DuplicateLabel`.
- **Validation errors** — raised after every file is parsed, once the
  whole story's scene graph exists. Examples: `BadJump` (a `->`
  target, choice target, check outcome, or puzzle outcome names a
  label that doesn't exist), `UnreachableScene` (a scene no `->`,
  choice, check outcome, or puzzle outcome ever reaches, starting
  from `start`), `UnknownAsset` (a `bg` or `show` name not in
  `assets.toml`), `UnknownSpeaker` (a dialogue speaker or `show`
  sprite not in `cast.toml`).
- **Validation warnings** — printed, but do not fail `check`:
  `MissingPuzzleDir` (a `puzzle <id>` with no `puzzles/<id>/` on
  disk yet).

`python -m linkloader check story/` exits `0` only when there are no
parse errors and no validation errors (warnings are fine).

## The JSON export schema

`python -m linkloader export story/ -o build/story.json` writes one
JSON object, meant for a future web runner:

```jsonc
{
  "start": "start",
  "scenes": {
    "<label>": {
      "statements": [
        {"kind": "bg", "name": "desert_night"},
        {"kind": "show", "sprite": "slim", "expression": "neutral", "position": "left"},
        {"kind": "hide", "sprite": "slim"},
        {"kind": "line", "speaker": "slim", "text": "..."},
        {"kind": "narration", "text": "..."},
        {"kind": "set", "assignments": [{"flag": "trust", "op": "+=", "value": 1}]},
        {"kind": "if", "condition": {"flag": "met_clipi", "op": "truthy"},
         "then": [ /* statements */ ], "else": [ /* statements, maybe [] */ ]},
        {"kind": "choice", "options": [
          {"text": "...", "target": "some_label", "condition": null}
        ]},
        {"kind": "check", "stat": "coder", "difficulty": 2,
         "outcomes": {"style": "label_a", "success": "label_b", "tie": null, "fail": "label_c"}},
        {"kind": "puzzle", "id": "count-crew",
         "outcomes": {"pass": "label_a", "lockout": null}},
        {"kind": "jump", "target": "some_label"}
      ]
    }
  },
  "cast": { "<id>": {"name": "..."} },
  "assets": { "bg": {"<name>": "<path>"}, "sprite": {"<id>": {"<expr>": "<path>"}} }
}
```

Notes for the runner author:

- `condition` and `outcomes` values are `null`, never an absent key,
  so a runner can always look them up without a presence check.
- Every `target`/label reference in this file has already passed
  `BadJump` validation — a runner does not need to re-check that a
  label exists.
- Asset paths are copied from `assets.toml` verbatim (paths relative
  to the repository root); the exporter does not rewrite them.

## One full example

```
== start
bg desert_night
show slim neutral left
slim: Satellite should be above us, now.
> The wind drops. Something on the horizon isn't moving right.
set met_clipi = false
choice
    "Call it in to Clipi." -> call_clipi
    "Take a closer look first." -> closer_look [if trust >= 1]

== call_clipi
show terminal idle right
terminal: Welcome, root. Please enter password.
set met_clipi = true
-> closer_look

== closer_look
hide terminal
check coder vs 2
    style -> found_it_clean
    success -> found_it
    fail -> jam_worse
puzzle count-crew
    pass -> found_it
    lockout -> jam_worse

== found_it_clean
> The chain unspools clean, no jam left behind.
slim: That's how you fix a loader.
-> ending

== found_it
slim: There. That'll hold.
-> ending

== jam_worse
if met_clipi
    terminal: Warning. Loader status: degraded.
else
    > No one's watching the line but you.
-> ending

== ending
> Another loader, linked. Somewhere out past delta-7, another one just jammed.
```
