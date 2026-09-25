# Rill — the loader-tongue

Rill is a conlang for a lonely space-cowboy mechanic. The grammar is
prefix. Every sentence is one s-expression: `(VERB ARG ARG ...)`.
There is no other sentence shape. Punctuation is parentheses. Rill has
no word for "please." Silence between jobs is the default register.

## Grammar roots (12)

These words ARE Scheme, under a different name. See
`puzzles/rill/prelude.scm` for the exact aliasing.

| Rill     | Scheme    | Gloss                                 |
|----------|-----------|----------------------------------------|
| `stake`  | `define`  | to stake a claim — name it            |
| `rig`    | `lambda`  | to rig — build a function             |
| `reckon` | `if`      | weigh a thing, choose a branch        |
| `bind`   | `cons`    | splice two things                     |
| `hesh`   | `car`     | the head, the lead car                |
| `tull`   | `cdr`     | the tail, what's towed behind         |
| `chain`  | `list`    | a chain of couplings                  |
| `sum`    | `+`       | add fuel                              |
| `less`   | `-`       | bleed off                             |
| `seal`   | `quote`   | seal it — don't run it, just hold it  |
| `husk?`  | `null?`   | is the hold empty, a husk?            |
| `same?`  | `equal?`  | same rig, same reading                |

## Thematic roots (8)

These are cargo, not code. They carry no grammar. Puzzles use them as
the data a sentence moves around.

| Rill    | Gloss              |
|---------|--------------------|
| `drev`  | star               |
| `mora`  | dust               |
| `kessa` | rope, tether       |
| `voth`  | wreck, dead husk   |
| `sil`   | signal             |
| `haan`  | kin, crew          |
| `dray`  | drift              |
| `fen`   | home, harbor       |

## Why the mapping holds

Every grammar root is aliased onto one Scheme primitive or special
form. Load the prelude, and a legal Rill sentence is a legal Scheme
s-expression. Lists, `car`/`cdr`, symbols, and recursion carry over
unchanged. This is the old "lists all the way down" lesson, re-skinned
for a mechanic who talks like she's tired.
