# find-signal — Find one good signal

The link loader has a chain of readings. Some are `voth` (dead
wrecks). At most one is a real signal — or none at all.

## Task

Write `find-signal` in Rill. It walks the chain and returns the first
element that is not `voth`. If the chain runs out, or is empty, it
returns `fen` (nothing left but home to go to).

Recursion only. Rill has no loops.

```scheme
(stake find-signal
  (rig (chain-in)
    (reckon (husk? chain-in)
            ___
            (reckon (same? (hesh chain-in) ___)
                    (find-signal (tull chain-in))
                    (hesh chain-in)))))
```

## Hint

Handle the empty chain first, then look at only the head of what is
left. Recurse on the tail when the head is a wreck; otherwise, that
head is your answer.

## Terminal

Work in `puzzles/find-signal/`. Copy `starter.rill` to `answer.rill`
and fill in the blanks. Check it:

```
bash puzzles/check/run.sh find-signal answer.rill
```
