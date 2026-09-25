# count-herd — Count the herd

The chest of drawers holds a chain of tags. Most are kin. A few are
planted wrecks, left there to throw the count off. Someone left two
grammar roots blank in an otherwise working Rill function.

## Task

Fill in both blanks. The first names the tag a wreck carries. The
second says what to hand the next call when an entry is kept in the
count.

```scheme
(stake herd-count
  (rig (chest)
    (reckon (husk? chest)
            0
            (reckon (same? (hesh chest) (seal ___))
                    (herd-count (tull chest))
                    (sum 1 (herd-count ___))))))
```

Bind your answer to the name `herd-count`, as a `rig` of one argument.

## Hint

The Lexicon marks one thematic root as a wreck, a dead husk. Test the
head of the chest against that root, sealed, with the grammar root for
"same reading."

When the head is a wreck, do not add to the count — just look past it.
When the head is kin, add one and look past it too. "Look past it"
means the same thing both times: hand the rest of the chest, not the
whole chest, to the next call. Handing the whole chest back to itself
never reaches the empty case.

## Terminal

Work in `puzzles/count-herd/`. Copy `starter.rill` to `answer.rill`
and fill in both blanks. Check it:

```
bash puzzles/check/run.sh count-herd answer.rill
```
