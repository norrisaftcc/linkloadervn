# count-crew — Count the crew

A chain (list) of kin needs a count. Someone left one grammar root
blank in an otherwise working Rill function.

## Task

Fill in the blank. Any grammar root that correctly tests "is this
chain empty" passes — not only the one word this puzzle was written
with.

```scheme
(stake haan-count
  (rig (roster)
    (reckon (___ roster)
            0
            (sum 1 (haan-count (tull roster))))))
```

Bind your answer to the name `haan-count`, as a `rig` of one argument.

## Hint

Look up the grammar root that answers "is the hold empty, a husk?" in
the Lexicon. It takes one argument and returns true or false.

## Terminal

Work in `puzzles/count-crew/`. Copy `starter.rill` to `answer.rill`
and fill in the blank. Check it:

```
bash puzzles/check/run.sh count-crew answer.rill
```
