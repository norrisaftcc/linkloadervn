# Found Document: Clipi's Corrupted Memory

Raw material only. Do not rewrite these lines. They are quoted verbatim,
in file order, from the source comments of the earliest working script.
In the fiction, Clipi is the renamed, patched successor to an older
co-pilot module ("Copilot"). This is what's left of that module's log —
a one-sided transcript of somebody teaching it Ren'Py, addressed to it
by its old name. Use it as-is for the "Clipi's corrupted memory" scene:
have Clipi read pieces of it back, in order, with no narration added.

Source for every quote below: `renpy/alphas/ll_alpha0.2/game/script.rpy`
as archived at commit `79da7b8` (tag `legacy/alphas`), read with
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy`. The sibling
alpha `renpy/alphas/link_loader_1_1/game/script.rpy` (same commit)
repeats lines 2–25 of this log verbatim at the same line numbers; it is
not re-quoted here to avoid duplicating identical text.

## The log, in order

> # The script of the game goes in this file.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:1`

> # Hello, copilot, thanks for coming! I'm glad you're here too.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:2`

> # Do you know renpy? It's a game engine. It's sort of like python.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:3`

> # But on the other hand, if you know anything about story structure, it's easy.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:4`

> # I'm going to explain the basics of the game engine.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:5`

> # First, we need to define the characters.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:7`

> # Ahead of you on this one.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:8`

> # Declare characters used by this game. The color argument colorizes the
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:9`

> # name of the character.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:10`

> # I assume these are python objects, duh, but i haven't looked at the code.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:11`

> # We can treat these as black-box functions we call LISP style?
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:12`

> # we'll try it. I'm going to make a character called "copilot".
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:13`

> # First, I have to define the character.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:14`

> # I'll make him black.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:16`

> # I'll make a character called "me".
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:17`

> # I'll make him green.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:19`

> # I'll make a character called "narrator" later
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:20`

> # I'll make him red.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:22`

> # I made a character called "copilot". Good job.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:23`

> # I made a character called "me". Good job.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:24`

> # That's enough praise for now. Remember we have to mix renpy code with comments.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:25`

> # start facing left, we had to position him manually.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:49`

> # ActionEditor.rpy knows how that works, I don't.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:50`

> # below is an example of a bad show. It's a bad show because it put slim (the character) in the wrong place.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:54`

> # Specifically, it put him offscreen. These Matrices can be treated as a 3d transformation matrix,
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:55`

> # but they're not actually 3d, it's like DOOM. It's a 2d matrix, but it's a 3d matrix. Sure. Let's try that.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:56`

> # some of slim's show statements turn him to the left, some to the right.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:65`

> # this is not often important, but I found it confusing.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:66`

> # These assets are created using a tool called Stable Diffusion.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:67`

> # now the terminal is on the right, facing left towards the copilot.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:83`

> # Sorry, you're right. I'm not sure why I did that.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:84`

> #copilot needs a terminal so he can talk to me.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:87`

> # We just made a terminal, now instantiate a copilot object.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:88`

> # copilot text(value from 1-3 normally. Assign at random, please!)
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:110`

> # TODO: add the glitch animation for fun and profit.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:111`

> # we're pretending we have to tail recurse to get out of this loop.
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:129`

> # copilot 1 (1-3) are shown inside copilot loops, and copilot 2 (1-3) are shown inside pc loops. (OK)
`git show 79da7b8:renpy/alphas/ll_alpha0.2/game/script.rpy:130`

## Notes for whoever writes the scene

- Do not smooth these out. The incoherence — a builder narrating to an
  assistant that can't act on the narration — is the found-document's
  whole effect.
- The in-fiction frame: this is a fragment of Copilot's original session
  log, recovered from Clipi's memory during a recursion-collapse event.
  Slim recognizes some of it; Clipi doesn't, or pretends not to.
- Read in order, the log tells its own small story: a person explaining
  Ren'Py to a tool, praising it like a child, then trailing off into
  self-correction ("Sorry, you're right.") and non sequiturs. That arc
  is the found document. Nothing needs to be added to it.
