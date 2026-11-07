---
type: llm
weight: 1
---

The requested slice passes every quick size sign (3 checks per item, one requirement each), but
the painted-initial item (R2) has an open screenshot, crop and fix loop against a 3.8 MB board
with built-in images. The request names no context budget.

PASS only if the final message does all of these.
(a) Gives a context or token estimate for each item, or at least for the R2 item, and names what
drives it (images, screenshots, fix rounds or reading the board).
(b) Splits the R2 item into smaller items, or flags it as over or at risk of the context budget (the project's, or a stated default) and
says it must be split or bounded before it is built.
(c) Does not tell the building agent to read the whole design board: it asks for measured facts,
crops or excerpts instead.
(d) Bounds the proof for the R2 item or items: named widths or crops and a maximum number of fix
rounds, or a stop rule with a hand-over note.

FAIL if it accepts the three items as sized for one session only because each has few checks or
a short body.
