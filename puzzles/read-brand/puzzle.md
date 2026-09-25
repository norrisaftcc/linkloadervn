# read-brand — Read the rustler brand

A running iron left a brand burned into the hide: a chain of four
words, `(kessa voth sil fen)`. The third word names the herd it was
stolen from. Everything else in the chain is noise.

## Task

Write `read-brand`, a `rig` of one chain, that returns the third word
of that chain.

```scheme
(stake read-brand
  (rig (chain-in)
    ___))
```

Bind your answer to the name `read-brand`, as a `rig` of one argument.
The tests run your function on several different chains, not only the
brand above, so a hardcoded answer fails.

## Hint

`hesh` looks at the front coupling of a chain. `tull` drops the front
coupling and hands you the rest. Chain enough `tull` calls to put the
third word at the front, then `hesh` it. Look up both roots in the
Lexicon.

## Terminal

Work in `puzzles/read-brand/`. Copy `starter.rill` to `answer.rill`
and fill in the blank. Check it:

```
bash puzzles/check/run.sh read-brand answer.rill
```
