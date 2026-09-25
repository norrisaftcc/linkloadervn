# decode-buoy — Transmission off the Fen buoy

A garbled transmission comes in off the Fen buoy. Five thematic
words, no grammar roots:

```
(sil drev mora dray fen)
```

## Task

Translate it word for word into English. Keep the order. Every word
in the transmission is a theme word — look each one up in the
Lexicon.

Bind your translation to the name `answer`, as a single sealed
(quoted) list of five English words.

```scheme
(stake answer (seal (word word word word word)))
```

## Hint

Translate one word at a time, left to right. The Lexicon's theme
table gives each word's gloss directly — no grammar root changes the
meaning here.

## Terminal

Work in `puzzles/decode-buoy/`. Copy `starter.rill` to `answer.rill`
and fill in the blanks. Check it:

```
bash puzzles/check/run.sh decode-buoy answer.rill
```
