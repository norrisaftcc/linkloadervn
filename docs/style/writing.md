# LinkLoader — Writing Style Guide

Status: v0.1. Covers docs, `CLAUDE.md`, issue and PR text, in-game UI
text, and puzzle instructions. Narrative prose (dialogue, scene text)
gets its own section below — it is allowed more room than the rest.

Two sources, used for different jobs:

- **Simplified Technical English (STE)** and **Orwell's six rules** for
  everything a reader must *act on correctly the first time*: docs,
  `CLAUDE.md`, issues, PRs, UI labels, puzzle prompts.
- **Gene Wolfe and Jack Vance** as touchstones for narrative prose only
  — Slim's voice, Clipi's corrupted memory, scene description. Their
  precision, not their difficulty, is the target.

## The rules for instructions and docs

From STE:

1. One instruction per sentence.
2. Active voice. "Rill checks your answer," not "your answer is
   checked."
3. Present tense for how things work; imperative for what to do.
   "Type your answer" — not "you should type your answer."
4. Keep sentences short. Instructions: under 20 words. Description:
   under 25.
5. Use the same word for the same thing, every time. Don't call it
   "the loader" in one line and "the terminal" in the next if they are
   the same object.
6. Write out the steps in the order the reader does them.

From Orwell (*Politics and the English Language*), applied here:

1. Never use a metaphor or figure of speech you have seen in print
   before. ("Deep dive," "leverage," "move the needle" — cut them.)
2. Never use a long word where a short one will do.
3. If a word can be cut, cut it.
4. Never use the passive where you can use the active.
5. Never use jargon or a foreign phrase if an everyday English word
   says the same thing.
6. Break any of these rules before you write something outright
   barbarous — the rules serve the sentence, not the other way round.

Together: short, active, concrete, one thought per sentence, same word
for the same thing. That is the whole standard for docs, `CLAUDE.md`,
issues, and PRs — no separate style is needed for those four.

## Narrative prose: Wolfe and Vance as touchstones

Gene Wolfe and Jack Vance are named for what they do well, not for
their vocabulary:

- **Precision over volume.** Both writers get a scene's weight from one
  exact, well-chosen detail, not from piling on adjectives. Slim
  describing a dead link loader should read like a mechanic who has
  seen forty of them, not like a tour guide.
- **The world is never explained to the reader.** Wolfe's narrators
  assume you already live there. Clipi's corrupted-memory fragments
  should read as genuinely found, not as a tutorial wearing a costume —
  they are allowed to be strange and slightly wrong, on purpose, the
  way a real corrupted log is wrong.
- **Formal or archaic diction is a spice, not a base.** Vance's
  characters can be ornate; the ornament earns its place because
  everything around it is otherwise plain. Use one unusual word where
  it counts, not five where it doesn't.
- **This license stops at the fourth wall.** A UI label, a puzzle
  prompt, or an error message is never the place for Wolfe-and-Vance
  diction. Those follow STE and Orwell without exception. Narrative
  license lives inside dialogue and scene text only.

## Before / after examples

### UI text

1. Before: "You are able to proceed to the next available terminal
   whenever you are ready to do so."
   After: "Go to the next terminal."

2. Before: "An error has occurred while attempting to save your
   progress."
   After: "Save failed. Try again."

3. Before: "Please utilize the puzzle editor in order to input your
   solution."
   After: "Type your answer in the puzzle editor."

### Puzzle prompts

1. Before: "The chain that has been provided to you contains a number
   of elements, some of which may potentially represent wrecks, and
   your task is to identify and return the first one that does not."
   After: "The chain has some wrecks (`voth`) and at most one real
   signal. Return the first element that is not `voth`."

2. Before: "It should be noted that recursion will be necessary in
   order to solve this particular puzzle, as loops are not a construct
   that exists within the Rill language."
   After: "Rill has no loops. Use recursion."

3. Before: "In the event that the chain is found to be empty, the
   correct behavior is for your function to return the symbol `fen`."
   After: "If the chain is empty, return `fen`."

### Dialogue

1. Before (over-explained): "Well now, partner, I reckon this here
   link loader's about as broken as broken gets, on account of the CDR
   rustlers having gotten to it first, if you catch my meaning."
   After (Wolfe/Vance precision): "Rustlers got to it first. Look at
   the `tull` — stripped clean." *(One exact detail does the work three
   sentences were doing.)*

2. Before (generic AI-assistant voice): "I have detected an anomaly in
   the current data stream. Would you like me to run a diagnostic?"
   After (Clipi, corrupted, in-fiction): "there was a — hold on — there
   was a shape in the — run it again, Slim. run it again."

3. Before (flat exposition): "The Company owns all the link loaders in
   this sector, and anyone caught tampering with one without a license
   will be fined or worse."
   After: "The Company's mark is on every loader out here. Touch one
   without papers and you're a rustler, whatever you meant to be."
