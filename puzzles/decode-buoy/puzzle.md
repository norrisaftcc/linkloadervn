# decode-buoy — Transmission off the Fen buoy

A garbled transmission comes in off the Fen buoy. Thematic words only.
No grammar roots.

```
(sil drev mora dray fen)
```

## Task

Translate it word for word into English. Keep the order. Use the
lexicon in `puzzles/rill/lexicon.md`.

Write your answer in `answer.rill` (copy `starter.rill` and fill it
in). Bind your translation to the name `answer`, as a single sealed
(quoted) list of English words.

```scheme
(stake answer (seal (word word word word word)))
```

## Check it

```
bash puzzles/check/run.sh decode-buoy answer.rill
```
