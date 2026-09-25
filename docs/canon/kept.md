# Kept: Lines and Jokes Carried Forward

Every line below is quoted exactly from an old script or note and is
canon-eligible for the revival. Nothing here is paraphrased. Where a
line appears in more than one draft with small wording changes, the
best-formed version is cited and the variants are named underneath it,
uncited (they are not separately verified quotes — see
`verify_quotes.py`, which only checks the blockquoted lines).

Source file for most of these:
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy` (the
current, 655-line script — the "Clipi" era, post-rename from Copilot).

## Voice and setting

> pc "Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:78`

Opening line. Keep it as the opening line. It does three jobs in one
breath: place (Syntax-4), sky (three moons), and voice (cowboy cadence,
"gonna").

> pc "Alright, time to head out. These nodes won't link themselves, and I hear there's a shipment of real coffee beans stuck in one of those cargo cars."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:181`

The "won't link themselves" pun is the title joke and should be kept
somewhere in every episode, not just this one.

> pc "Yes, and run a diagnostic on our repair tools. We'll need the parenthesis patcher and the recursion breaker for sure."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:190`

Named tools worth keeping as actual Rill-puzzle equipment, not just a
throwaway line: "the parenthesis patcher" and "the recursion breaker."

## The terminal gag

> pc "(sudo restart satellite)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:119`

> t "Welcome, root. Please enter password:"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:122`

The sudo/root/password beat is the best-integrated tech gag in the
script — it's an actual shell interaction played as a customs
checkpoint. Keep the beat; the literal "********" line is filler and
does not need to survive verbatim.

> t "git pull: Loading new coordinates and repair protocols..."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:172`

> pc "Finally! This connection is slower than a turtle in molasses."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:175`

`git pull` as "the mail's here" is a good running bit for the Terminal.

## The recursion-collapse beat (Clipi's fragility)

> pc "Careful with that phrase, Clipi. Remember what happened last time you got stuck in a recursive language pattern."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:153`

> clipi "I'm not in the (loop). I'm not in the ((loop))."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:159`

This is the core bit — "I'm not in the loop" as a phrase that, spoken
near an AI built on Rill/Scheme, triggers literal unbounded recursion
(the parentheses nest with every repetition). It's the single best joke
across every draft of this script, present from `ll_alpha0.2` onward,
and it should be the spine of the dedicated Clipi segment, not just a
gag in scene 1.

## The LISP-nonsense diagnosis

> clipi "Scanning... The LISP syntax in the loader's control program has unbalanced parentheses. It's trying to execute: (load (car (cdr (cons))))"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:234`

> pc "That's nonsense code. There's nothing inside the innermost function."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:237`

`(load (car (cdr (cons))))` is a genuinely well-formed piece of broken
Lisp — `cons` with no arguments is exactly the kind of error a Rill
puzzle should present to the player. Keep the literal expression as a
template for a puzzle's starting (broken) sentence.

## The Sh- robot dialect

> cargo_bot "(Sh-query maintenance status sh-current sh-loader)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:240`

> rustler "(Sh-greetings troubleshooter sh-your services sh-no longer required)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:475`

> rustler "(Sh-we are sh-cdr collective sh-we liberate data from sh-closed loops)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:481`

> rustler "(Sh-not stealing sh-redistributing sh-information wants to be free sh-cargo wants to be free)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:487`

> rustler "(Sh-clever human sh-this round sh-to you)"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:518`

The "sh" = spoken parenthesis speech rule is the strongest piece of
worldbuilding here. "Information wants to be free, cargo wants to be
free" is the rustlers' whole ideology in one line — keep it exactly,
it's their best joke and their most sincere one at the same time.

## The rustler reveal and the joke name

> clipi "Running git blame on loader firmware... Last modifications made by user 'cdr_rustler42'."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:309`

> pc "CDR rustlers! I should have known. They're stealing cargo by manipulating the link loaders."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:312`

> pc "CDR rustlers! Those parenthesis-thieving varmints!"
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:357`

`git blame` as a detective move, landing on a joke username
(`cdr_rustler42`), is a keeper. "Parenthesis-thieving varmints" is the
best pure-Western/pure-Lisp pun in the whole script and should be kept
verbatim somewhere in the new dialogue.

## The coder-approach poetry line

> pc "It's all about understanding the flow. Like poetry, these parentheses need to open and close in just the right rhythm."
`renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game/script.rpy:379`

Good statement of theme in-voice: Rill puzzles should feel like this
line describes them.

## Stats and character creation (from the design notes, pre-script)

> (cons car cdr) -> (car cdr)
`media/rules_notes.md:18`

> Cosmonaut Cowboy Coder Person (CCCP)
`media/rules_notes.md:24`

> aka (((P)))
`media/rules_notes.md:25`

> so (((P))) is "sh-sh-sh-p"
`media/rules_notes.md:35`

CCCP / (((P))) is the founding joke of the whole project — the
player's title is itself a Lisp expression. Keep the acronym and the
triple-paren joke; the game's three stats (Cosmonaut, Cowboy, Coder)
come directly from unpacking it.

> If you have low coder, you just say "shucks" a lot and never noticed parentheses.
`media/rules_notes.md:39`

Good design instinct already present in the notes: low Coder should
change how much of the Sh- dialect the player character even perceives,
not just their skill in using it. Worth carrying into the new stat
mapping (see `bible.md`).
