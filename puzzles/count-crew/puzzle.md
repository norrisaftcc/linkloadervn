# count-crew — Count the crew

One grammar root is missing from a working Rill function. It counts a
chain (list) of kin.

```scheme
(stake haan-count
  (rig (roster)
    (reckon (___ roster)
            0
            (sum 1 (haan-count (tull roster))))))
```

## Task

Fill in the blank. Any grammar root that correctly tests "is this
chain empty" will pass — not only the one word this puzzle was written
with.

## Check it

```
bash puzzles/check/run.sh count-crew answer.rill
```
