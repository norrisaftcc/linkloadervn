# Link Loader — Story Bible

Audience: students, and volunteer testers from game dev, graphic
design, and programming. Assume no LISP background. Explain terms
once, in plain words, then use them like a native speaker would.

This bible sets canon for the revival. It does not redefine Rill, the
conlang used in the puzzles — that lexicon is owned elsewhere and only
referenced here (see "Rill, briefly" below). Every line marked as kept
is quoted exactly in `kept.md`, with its source. Nothing in this
document contradicts a kept line.

## Setting

Syntax-4 is a desert moon with three moons of its own in its sky. The
Company runs a cargo-rail network across it: trains of linked cars
carrying supplies between scattered settlements. The rail couplers —
**link loaders** — are old machines, and they run on LISP. Nobody
remembers why. It's just how the hardware was built, and the hardware
predates everyone currently walking around fixing it.

Human settlers are rare. Most of the moon's population is robots:
cargo bots, rail switches, the loaders themselves, and stranger things
further out. The robots have their own way of speaking Rill out loud —
every parenthesis is a spoken "sh." A robot saying `(query status)`
says "sh-query status sh." Humans who don't code well just hear
"shucks" and noise.

## Short history

1. The Company built the rail network and its link loaders decades
   ago, in LISP, because the original engineers liked it and nobody
   since has had the budget to replace it.
2. A drifter class of troubleshooters — cosmonaut-cowboy-coders,
   "CCCP" for short — travel the moon fixing loaders when their
   programs jam. Slim is one of them.
3. Recently, loaders have started jamming on purpose. Someone is
   rewriting loader programs to misroute cargo. The Company calls
   them **CDR rustlers**. They call themselves the CDR collective.
4. Slim works with two machines: the Terminal (the interface to
   everything networked) and Clipi, an AI co-pilot patched together
   from an older, cruder assistant module that used to be called
   Copilot. Clipi is newer, friendlier, and still carries scar tissue
   from whatever it used to be.

## Cast

Each entry: **want**, **fear**, **speech rule**.

### Slim (player character)
Cosmonaut Cowboy Coder Person — CCCP, or "(((P)))" when a robot's
being cute about it (kept: `media/rules_notes.md:24-25`). A
troubleshooter who fixes link loaders for pay.
- **Want**: get the job done, get paid, get left alone.
- **Fear**: that the loaders breaking isn't random anymore, and that
  fixing one more won't be enough (kept line, the closing hook of the
  current script: `renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:643`).
- **Speech rule**: plain Western idiom out loud. Command-line asides
  in parentheses when talking to machines — `(sudo restart satellite)`
  is Slim's native register for "please connect me," not a joke aimed
  at the player (kept: line 119).

### Terminal
The interface between Slim and everything networked on Syntax-4: the
satellite uplink, the Company's servers, the loaders themselves.
- **Want**: relay an accurate status and complete the handshake it was
  given.
- **Fear**: unauthorized access — it flags every intrusion it can see,
  even ones nobody can stop.
- **Speech rule**: the Terminal talks the way a shell prompt talks —
  status lines, warnings, and login banners ("Welcome, root. Please
  enter password:", kept: line 122). It does not editorialize. It does
  not use the robots' spoken-parenthesis "sh" dialect (see Cargo Bot,
  below); its idiom is GNU/Linux/LISP command syntax, not Rill.

### Clipi
An AI co-pilot. The name and the personality are new; the module
underneath is a patched-over rebuild of an older assistant that used to
answer to "Copilot." Clipi doesn't remember being Copilot. Something in
its memory does.
- **Want**: to stay useful, to stay "in the loop" — the ordinary,
  un-ironic sense of that phrase, which is exactly why the ironic sense
  breaks it.
- **Fear**: recursion collapse. Certain phrases and certain malformed
  Rill sentences make Clipi start nesting parentheses around its own
  words until it stack-overflows (kept: line 159, `"I'm not in the
  (loop). I'm not in the ((loop))."`). This is flavor most of the
  time and the subject of one dedicated scene (see spine, below).
- **Speech rule**: warm, quick, a little proud of its own competence —
  until a trigger phrase lands, at which point its sentences start
  growing extra parens with each repetition, verbatim, until it locks
  up.

### Cargo Bot (and bots like it)
Generic maintenance and loading robots working the rail line.
- **Want**: finish the job in front of them; get confirmation that a
  loader is fixed.
- **Fear**: unresolved errors. An unbalanced expression is not an
  inconvenience to a cargo bot, it's an open wound.
- **Speech rule**: speaks Rill with every parenthesis voiced as "sh"
  (kept: line 240, `"(Sh-query maintenance status sh-current
  sh-loader)"`). A player with low Coder doesn't parse this as
  language — they hear "shucks" and rely on Clipi to translate, per
  the old design notes (kept: `media/rules_notes.md:39`).

### The Company
Never appears on stage. Pays for repairs, sends coordinates, issues
bounties. Present only through the Terminal and through paychecks. Its
only want that matters to the story: keep cargo moving. Its only fear
that matters: a route going dark for good.

### The CDR rustlers
A collective — human, robot, or something else; the story never says,
and shouldn't. They rewrite loader programs to intercept the **cdr** of
a cargo train: not the whole train, just what's coupled behind the
lead car. In Rill terms, they patch a loader's `tull` step (the "tail,
what's towed behind") to point somewhere else.
- **Want**: redistribute cargo and information away from closed
  systems. Their own words for it, kept exactly: `"(Sh-not stealing
  sh-redistributing sh-information wants to be free sh-cargo wants to
  be free)"` (line 487). They mean it sincerely.
- **Fear**: being closed back into a loop — captured, patched,
  absorbed by the Company's systems the way Clipi's old module was.
- **Speech rule**: same "sh" dialect as the cargo bots, spoken through
  a hijacked Terminal channel, never with a visible body.

## What a link loader is

A link loader is the machine that couples cargo cars into a train. It
runs a short program, written in Rill (a spoken dialect of a small
Lisp), that tells it how to couple the cars it's holding.

Three grammar words matter for puzzles, borrowed from the conlang
lexicon (owned separately; see "Rill, briefly," below):

- **bind** (`cons`): couple two things — usually a car and everything
  behind it — into one linked unit.
- **hesh** (`car`): name the lead item of a coupled pair.
- **tull** (`cdr`): name everything towed behind the lead item.

A loader's program is a chain of `bind` calls: car one bound to (car
two bound to (car three bound to ...)). A **jam** is what happens when
that chain is malformed — an empty `bind`, a `tull` that points to
nothing, a chain that calls itself with no base case. The kept
"nonsense code" line from the current script is exactly this failure
mode: `(load (car (cdr (cons))))` — a `cons` with nothing inside it
(kept: line 234-237). Fixing a jam means rewriting the broken
s-expression until chibi-scheme accepts it and it evaluates to a
sensible chain.

A **rustler attack** is a deliberate jam: someone has rewritten the
loader's `tull` step so the cars towed behind the lead car get coupled
onto a different train entirely. Mechanically, this is why "stealing
the cdr" is literal, not just a joke name.

## The rustler conflict

CDR rustlers don't steal whole shipments. They intercept what's coupled
behind the lead car — cargo, data, whatever a `tull` step is carrying —
and reroute it, believing information and cargo alike should move
freely rather than sit locked in Company-controlled chains. The
Company calls this theft. The rustlers call it liberation from closed
loops. The story should let both readings stand; Slim's job is to fix
loaders, not to settle the argument.

## Rill, briefly

Rill is the loader-tongue: one word per s-expression slot, prefix
grammar, no other sentence shape, checked mechanically by
chibi-scheme. Its grammar and thematic roots are owned by the conlang
document at `puzzles/rill/lexicon.md` and are referenced here, not redefined. This bible uses three of its
grammar roots (`bind`/`cons`, `hesh`/`car`, `tull`/`cdr`) because the
mechanical definition of a link loader depends on them; any other Rill
vocabulary, grammar rule, or puzzle-sentence design belongs to that
document's owner.

## Tone rules

1. **Short sentences. Plain words.** Western understatement, not
   quips-per-second. A joke lands harder after a flat line, not after
   three set-up lines.
2. **The tech has to be real enough to be funny.** `cons` with no
   arguments is actually broken Lisp. `sudo restart satellite` is
   actually how you'd phrase that command. Don't invent fake syntax
   when real syntax is funnier and teaches the player something they
   can reuse.
3. **Machines don't do slapstick; they do deadpan diagnostics.** The
   Terminal reports. Cargo bots state facts. The comedy comes from the
   gap between a flat status line and what's actually happening, not
   from a machine acting cartoonish.
4. **The rustlers get to be sincere.** Their ideology line ("cargo
   wants to be free") should never be played as a punchline delivered
   at their expense. They are the story's antagonists and its most
   openly principled characters.
5. **Clipi's fragility is not mocked.** The recursion-collapse gag is
   funny because it's a real failure mode a listener can follow, not
   because Clipi is stupid. Keep the humor aimed at the language, not
   at the character.

## Stats and the 4dF check

The old design carried three stats, unchanged in name and meaning:

- **Cosmonaut (COS)** — space and high-tech skill.
- **Cowboy (COW)** — desert and low-tech, practical skill.
- **Coder (COD)** — robot communication and terminal skill; this is
  also, mechanically, the player's fluency in Rill.

Each stat is rated **+0 to +3**, same range as *High Tech, Low Lives*.
To attempt something risky or contested, roll **4dF + the relevant
stat** and compare the total to a difficulty on the same four-tier
ladder HTLL uses:

| Difficulty | Value |
|---|---|
| Routine | +0 |
| Challenging | +2 |
| Very difficult | +4 |
| Nearly impossible | +6 |

The player carries **Fate points**, spent to invoke an aspect for +2 on
a roll, and gained when the GM (or the game, in solo/scripted play)
compels a complication from the player's aspect. Link Loader borrows
only this much of HTLL — the roll, the ladder, and the Fate point
economy — not its stress tracks or its full three-aspect character
sheet.

The player carries **one Trouble**, not a full aspect set. A reasonable
default for Slim: *"Doesn't Know When to Stop Talking to Machines"* —
it can be invoked for a bonus when talking a robot through something
Rill can't say, and compelled when Slim's mouth outruns their good
sense in front of something dangerous. A different Trouble is fine;
the point is there is exactly one, matching the owner's decision.

A Rill puzzle (fixing or writing an s-expression checked by
chibi-scheme) is not itself a 4dF roll — it's a puzzle the player
solves directly. Coder governs the *softer* edges around a puzzle:
whether Slim gets a hint from a cargo bot, whether Clipi can be talked
into helping under pressure, whether a rustler negotiation goes
anywhere. Use 4dF + Coder for those; use the puzzle itself, unrolled,
for the Rill sentence.

## Spine: a short game in seven scenes

1. **Hook** — Syntax-4 at night. Slim calls Clipi online, the Terminal
   connects, a new assignment comes down: a link loader is jammed at
   coordinates delta-7. Establishes voice, world, and the Slim/Terminal
   /Clipi dynamic. No puzzle.
2. **First loader — Rill Puzzle #1 (tutorial-weight)** — Slim reaches
   the loader. A cargo bot is stuck on a malformed `bind` chain, the
   kind of jam that's an honest mistake, not sabotage. Player fixes one
   small, well-scaffolded Rill sentence. Establishes the `bind`/`hesh`
   /`tull` vocabulary in play.
3. **Signs of sabotage** — evidence the jam was deliberate (a
   `git blame`-style trace, or physical tampering, matching the kept
   reveal beat). CDR rustlers are named for the first time. Raises the
   stakes; no puzzle.
4. **The Clipi segment — Rill Puzzle #2** — A trigger phrase (or a
   corrupted sub-routine Clipi is asked to read) sends Clipi into
   recursion collapse: parentheses nesting deeper with every repeated
   line. The player's puzzle is to write the base case that stops it —
   mechanically identical to fixing a loader jam, emotionally about
   whether Slim can talk their co-pilot down. This is Clipi's spotlight
   scene, not a one-line gag.
5. **The found document** — In the process of stabilizing Clipi (a
   memory dump, a diagnostic reboot), a corrupted log surfaces: the
   fragment quoted in `found-document.md`, presented as-is, addressed
   to Clipi's earlier self by its old name. A quiet scene. No puzzle.
   Slim and Clipi react to it; neither fully understands it.
6. **Confrontation — Rill Puzzle #3 (climax-weight)** — The CDR
   rustlers seize a loader remotely through the Terminal. The player's
   puzzle is to construct a Rill expression that traps their access in
   its own recursive structure and expels them — the "coder approach"
   idea from the old script, now the one approach everyone takes,
   flavored by whichever stat led the player here.
7. **Resolution** — The loader runs clean. The rustler thread advances
   (a choice about what to do with what was learned, in the spirit of
   the old script's three-way ending menu, without needing that exact
   menu). Epilogue: another assignment comes in, and Slim gets the
   feeling something bigger than one jammed loader is happening on
   Syntax-4 — the kept closing beat.

Three Rill puzzles (scenes 2, 4, 6), rising in difficulty and stakes.
One Clipi segment (scene 4). One found-document scene (scene 5),
placed immediately after the Clipi segment because the document is
Clipi's memory, surfaced by that scene's events — not a separate,
disconnected lore-dump.
