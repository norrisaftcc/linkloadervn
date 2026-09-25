# rebalance-coupling — Rebalance the coupling

A coupling is a chain of links. A few links are wrecks, wrecked husks
left in the line by the sabotage. The rest have to run in the same
order they came in, just with the wrecks gone. Someone left three
grammar roots blank in an otherwise working Rill function.

## Task

Fill in all three blanks. The first is what an empty coupling rebuilds
into. The other two both belong to the same sentence: what goes on the
front of the rebuilt chain, and which links get run through
`rebalance` again to build the rest.

```scheme
(stake rebalance
  (rig (links)
    (reckon (husk? links)
            ___
            (reckon (same? (hesh links) (seal voth))
                    (rebalance (tull links))
                    (bind ___ (rebalance ___))))))
```

Bind your answer to the name `rebalance`, as a `rig` of one argument.

## Hint

An empty coupling rebuilds into an empty coupling — there is a grammar
root that builds a chain out of nothing.

When the head of the coupling is a wreck, skip it: rebalance the rest
and stop there, nothing gets added on. When the head is sound, it
belongs at the front of the rebuilt chain, ahead of whatever the rest
of the coupling rebuilds into. The grammar root for "splice two things
together" puts one thing in front of another; use it to put the head
in front of the rebuilt rest, not the rest in front of the head. In
both places you rebuild "the rest," you mean the same thing: the
coupling with its head towed away, not the whole coupling handed back
to itself.

## Terminal

Work in `puzzles/rebalance-coupling/`. Copy `starter.rill` to
`answer.rill` and fill in all three blanks. Check it:

```
bash puzzles/check/run.sh rebalance-coupling answer.rill
```
