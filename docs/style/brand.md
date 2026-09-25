# LinkLoader — Visual Brand Guide

Status: v0.1, first draft from the founding spike. Audience: students and
volunteer testers in game dev, graphic design, and programming.

This guide follows the **spike-to-system** method: name the perspectives
the reference pile suggested, pick one, then write it up as rules a
computer or a new contributor can follow without asking us first.

---

## Rule 0 — authority order

When a rule here conflicts with something else, this order wins:

1. **Produced game art** that we keep — the four Stable Diffusion sprites
   named in this guide (`slim neutral.png`, `terminal idle.png`, `clipi
   talk.png`, `bg desert night.png`) and any bug found in them.
2. **The owner's decisions**, listed in the project brief (Rill, the
   4dF ladder, the Pelican/mainframe-comic look).
3. **The AlgoCratic Design System v0.2**, which we treat as a sibling
   system to reuse token names and values from, not a parent to inherit
   from blindly.
4. **The Pinterest board and the two comics** — direction, not decisions.
   Nobody is asked to find a font called "Spiral Dynamics."

---

## Phase 1 — what the spike actually says

Sorted by the tiers above:

- **Produced**: the four sprites are full-color, airbrushed, high-detail
  AI renders — the opposite of the flat mid-century look the board asks
  for. Every cut-out sprite also shipped a magenta halo: a rim or glow
  left along the silhouette by the magenta chroma key. That was not a
  style choice. `tools/assets/despill.py` removes it, and it is why this
  guide states a hard rule about magenta below.
- **Canonical document**: AlgoCratic Design System v0.2. It already has a
  "Pelican stratum" — flat, print-column, paper-backed — proven to
  survive a hostile renderer (the Canvas sanitizer). We reuse its
  paper/ink relationship and its "always pair background+color" rule.
- **Aspirational, and why each piece is there** (the tells):
  - Pelican covers, "The Spell of Mathematics," the probability-dice
    grid: flat geometric shapes, one bold color plate, a single graphic
    idea per cover. This is a *composition* argument, not just a palette
    one.
  - The atom-eye poster: a single iconic mark can carry a whole cover.
    Link Loader's puzzle icon or Rill glyph should aim for the same
    one-mark-says-it-all economy.
  - Cobalt Confessions and the B.I.A. mainframe comic: halftone ink,
    heavy panel borders, comic lettering, and — this is the real tell —
    *found-document* framing (an in-universe artifact someone is
    reading, not the game's own chrome). This is a **channel** argument:
    it proposes a second voice, not a second palette for buttons.
  - Spiral Dynamics: almost certainly on the board for its rainbow
    spiral graphic, but the book's actual idea — each stage transcends
    *and includes* the one before it — is a better fit as a **mechanic**
    than as a color scheme. Rainbow UI is explicitly rejected below.
  - Touretzky's *Common Lisp*: confirms the Rill conlang's own framing
    ("lists all the way down") and licenses a Lisp-adjacent visual
    vocabulary — parentheses, s-expressions, dot-grid — as legitimate
    puzzle-panel decoration, not just code.

---

## Phase 2 — perspectives considered

**A. Canon-inversion.** Treat the shipped sprites as the real style
guide and reverse-engineer rules from them. Rejected as the *whole*
answer — the sprites disagree with the brief's own "Pelican-book
modernism" instruction, and one of them is actively bugged. Kept as a
**constraint**: whatever system we pick has to have a real answer for
how these specific sprites sit inside it (see "Sprites in the system,"
below) and has to fix the magenta bug, not paint over it.

**B. Channel/voice reading.** The comics are not the game's UI language;
they are what a *found document* looks like inside the fiction. Kept —
this becomes Clipi's corrupted-memory register.

**C. The organizing frame — two strata, one system.** Pelican-book
modernism (flat geometry, one clean sans, a short restrained palette) is
the **outer stratum**: menus, the dialogue box, choices, docs, the
puzzle editor chrome. 1960s mainframe-comic ink (halftone, heavy line,
comic lettering) is an **inner stratum**, used only for diegetic
found-document moments — Clipi's corrupted memory, old Company
bulletins, salvage-yard signage. **Chosen.** It resolves A vs. B without
averaging them into mush, and it makes Link Loader a legible sibling of
AlgoCratic's own Pelican/Underground split — same shape, different
meaning. AlgoCratic's split is *surface-corporate vs. resistance
voice*; Link Loader's is *interface vs. diegetic artifact*. State the
difference plainly so nobody assumes the semantics carried over with the
name.

**D. The mechanic — accretion, not rainbow.** Spiral Dynamics'
"transcend and include" becomes a rule for how the *player's own
information* accretes (a completed puzzle's Rill stays visible, folded
into the next panel, rather than replaced) — never a rule for coloring
buttons by "level." Kept as Rule 6 below.

**Ranking**: C is mandatory — it is the whole shape of the system. A's
magenta-bug constraint is non-negotiable (real users will see a real
glitch if we skip it). D is the sleeper: cheap to implement, and it is
the one idea in this guide that came from a management book nobody
expected to matter. B has the biggest open question: exactly how much
mainframe-comic ink survives contact with a browser and a phone screen
(see "Open questions").

---

## Phase 3 — the system

### 1. Palette

Reused from AlgoCratic v0.2 (◆ = same value, not just same idea):

| Role | Token | Hex | Source |
|---|---|---|---|
| Paper (page/panel ground) | `--color-paper` | `#F3EDDC` | New — AlgoCratic's paper tokens (`#F5F0E6`, `#F2F7F5`) are cooler; ours is warmer to read as desert, not lab. Same *role*, different value — noted, not silently swapped. |
| Ink (default text) | `--color-ink` | `#1A1A1A` | New. AlgoCratic uses near-black too; value differs slightly, role identical. |

New to Link Loader (AlgoCratic v0.2 has no equivalents — these are not
overrides, they are additions):

| Role | Token | Hex | Notes |
|---|---|---|---|
| Teal (Terminal, machine-cool, the Company) | `--color-teal` | `#1B4D5C` | Same hex as the *Infiltrator* playbook color in High Tech, Low Lives — a deliberate crossover, both are "corporate cold." |
| Orange (Slim, desert warmth, western) | `--color-orange` | `#B84A25` | Muted down from a pure Pelican-cover orange so it reads on a cream page without vibrating. |
| Magenta (Clipi, glitch, danger) | `--color-magenta` | `#951655` | See the hard rule below. Deep enough to hit 4.5:1 on paper as a badge fill; never used as a light glow value. |
| Ochre (Cargo Bot, sand, rust) | `--color-ochre` | `#8A6415` | Body-text-legal on paper (4.59:1) — kept deliberately close to the AA floor rather than brightened, so it stays a *dusty* accent, not a warning color. |
| Deep paper (panel-on-panel) | `--color-paper-deep` | `#EAE0C4` | For a panel that needs to sit visually behind the page paper — a card, an inset. |
| White | `--color-white` | `#FFFFFF` | For text on the darker fills (teal, magenta, orange chips). |

**Pairing rule (reused from AlgoCratic verbatim):** every color chip,
badge, or clearance-style tag sets both `background` and `color`
together. A badge that loses its fill in a high-contrast mode must not
turn into unreadable text on the page's own background.

**Hard rule — magenta is a flat fill, never a glow.** No
`box-shadow` bloom, no `filter: drop-shadow`, no gradient-to-transparent,
no semi-transparent magenta over a light-transparent edge. The old game
shipped exactly this bug: a chroma-key halo around every Clipi, Slim
and terminal cut-out. Any new sprite must pass
`python tools/assets/despill.py --scan` before it goes in the game. Magenta appears
only as: solid text, a solid badge fill, or a solid rule/border. Never
as a shadow, an outer glow, or an edge treatment.

### 2. Type — free fonts only

| Role | Token | Face | Why |
|---|---|---|---|
| Display / headers | `--font-display` | **Space Grotesk** | Geometric, a little mechanical, reads "terminal" without going full sci-fi-chrome. Divergence from AlgoCratic: they use Orbitron for display. Orbitron reads as *clean future-corporate*; we want *1968 mainframe pulp*, which is grittier. Different course, different register — same reason SHODANN kept her own voice in the Canvas fork. |
| Body | `--font-body` | **IBM Plex Sans** | Reused role and reasoning from AlgoCratic (their body face is Plex Sans too) — humanist, highly legible, and "IBM" is a nice quiet joke in a mainframe game. Same family as `--font-mono` below, so body and code visually belong together. |
| Mono (Rill, terminal output, Clipi's corrupted-memory transcripts) | `--font-mono` | **IBM Plex Mono** | Reused rule from AlgoCratic: monospace signals *a machine actually emitted this*. Rill code blocks, chibi-scheme output, and terminal chrome all use it; a human character never does. |

All three are on Google Fonts, free, and self-hostable if the build
later needs to drop the CDN.

### 3. Geometry and composition

1. **Flat shapes, hard edges.** No drop shadows, no soft gradients, no
   bevels. A shape is one flat color plate, outlined or not.
2. **One graphic idea per screen**, borrowed from the Pelican covers —
   a background, a character, a UI panel: pick the one shape that
   carries the beat, don't stack three competing ones.
3. **Thick, consistent outline weight** on any redrawn or vector art —
   think the atom-eye poster's line, not airbrush.
4. **A grid, always visible or implied.** The probability-dice grid and
   the Lisp cover's dot-lattice both license a visible grid as
   *decoration*, not just a layout tool — the puzzle panel (below) uses
   this directly.
5. **No rainbow gradients as a system.** Spiral Dynamics' stripes stay
   in the book. See Rule 6.
6. **Accretion, not replacement.** When the player clears a puzzle, its
   solved Rill form stays visible (smaller, folded into a margin or
   header) in the next panel, rather than disappearing. Each stage
   contains the one before it — the one idea worth keeping from the
   Spiral Dynamics reference.

### 4. Sprites in the system — how the SD art sits inside this

The existing Stable-Diffusion sprites (`slim neutral.png`, `terminal
idle.png`, `clipi talk.png`, `bg desert night.png`, and their siblings
in `game/images/`) are airbrushed and full-color — the opposite of Rule
1. Two things happen to any sprite that ships:

1. **Duotone pass.** Convert to grayscale, then map shadows to
   `--color-ink` and highlights to the sprite's assigned accent (Slim →
   orange, Terminal → teal, Clipi → magenta, Cargo Bot → ochre). This is
   the same recipe already named in the project's own visual-design
   requirements for the *High Tech, Low Lives* playbooks — reused here
   deliberately, since both projects want "duotone ink line art."
2. **Flat color plate behind the cutout.** Crop the sprite to its
   silhouette, then place it in front of a single flat rectangle in
   `--color-paper-deep` (or the accent color at low enough weight to
   still pass Rule "magenta is a flat fill" if the accent is magenta —
   in practice, never put a flat magenta plate directly behind Clipi;
   use paper-deep and let the duotone highlight carry the magenta).

This is a **generative rule**, not a one-off Photoshop job — the next
sprite (Syntax-4, a rustler, a new NPC) gets the same two passes, in
this order, and comes out a family member. `tools/assets/despill.py`
does the despill half of step 1; a full duotone pipeline is a pending
input (see below).

### 5. UI rules

- **Dialogue box.** Flat `--color-paper-deep` panel, `--color-ink` body
  text in `--font-body`, a thin 2px rule in the speaking character's
  accent color along the top edge only (not a full border — a full
  colored border on every box gets loud fast). The speaker's name sits
  in `--font-display`, small caps, in that same accent color, paired
  with `--color-paper` behind it per the pairing rule if it's ever a
  filled chip.
- **Choices.** A flat list, no card shadows. Each choice is a row with
  a 1px `--color-ink` bottom rule; the hovered/selected choice gets a
  solid `--color-orange` left bar (3–4px), never a full-row fill —
  keeps the "one flat idea" reading instead of a button-soup.
- **Puzzle editor (Rill).** Monospace, `--color-ink` on `--color-paper`,
  laid over the faint dot-grid from Rule 4 (the grid sits *behind* the
  code at ~8% opacity — decoration, never a legibility hazard). Parens
  depth can be lightly weighted (heavier stroke on the outermost pair)
  since Rill sentences are s-expressions and depth *is* the grammar —
  but never color-code parens by rainbow depth (see Rule 5). Errors from
  chibi-scheme surface in a flat `--color-magenta` text chip
  (background+color paired, per the hard rule — never a red squiggle,
  never a glow).

---

## Open questions (pending inputs to bump this to v0.2)

- Real duotone passes on all four hero sprites, and a decision on
  whether Cargo Bot and Syntax-4 get new renders or duotone treatment of
  what exists.
- An actual Rill glyph or wordmark — a single "atom-eye"-grade icon.
- How much mainframe-comic ink survives on a 390px phone screen before
  the halftone just reads as noise (test with real testers, not a
  guess).
- Decided: the pale yellow haze on `terminal talk.png` and its siblings
  is intended CRT glow. It stays. `despill.py` does not touch it.
