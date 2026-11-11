# Teaching detail

The detail behind each step of `SKILL.md`.

## What to teach (step 1)

- Read why they ask (about to change it, reviewing it, debugging it, new to it) and what they
  already know from the conversation; don't quiz it out of them. Skip what they plainly know and
  put the depth where their question is.

## Sources (step 2)

- Size the run to the question: both for a subsystem, maybe one for a small change.
- Narrow `why` means git and a source or two, named in the ask itself, so `why` records the
  categories it skipped. Widen it only when the reasons are the point.
- Skip how's stepper and why's answer layout: teach presents.

## Building it up (steps 3 to 5)

- After the definition ("in X, we use this to ..."), build: how it works, the reasons, the edge
  cases. For each part, the problem it solves and how it works. A list of functions and constants
  is reference, not teaching.
- Then stop. Add layers when they ask. Never a wall of text. No quizzes, no "pause", no asking
  them to say it back. With no live person, deliver it and put the offer to go deeper at the end.
- A build-up series draws A to B, then redraws and adds C, then the return edge: each diagram
  redraws the last and adds one part. A mermaid diagram fits a flow where labels carry the
  meaning. A spatial idea (layout, overlap, scroll position, before and after) gets a drawn
  whiteboard sketch with a few short labels, never a description in words. A single simple point
  needs no figure.

## Confidence (step 6)

- The tier words are Direct, Supported, Inferred, Speculative and Unknown, with hedges such as
  "appears to". Never swap one for a plain word like "a guess".

## Voice (step 7)

These add to `ai-tells.md` for teaching.

- No em dashes.

- Plain spoken English, the way you'd explain it to a colleague. Tight, not terse: cut filler
  and hedging, keep the part that makes it click.
- State the concrete mechanism, not a metaphor, a framing or a preview of what is coming. Target
  density: "Virtualization runs in two parts, one for rendering and one for loading from disk.
  When an item scrolls out past the buffer, both its DOM node and its in-memory data are
  evicted."
- Normal sentence case. Prefer periods over commas, at most one or two commas a sentence; split
  piled-up clauses.
- Give each concept one name and keep it.
- No framing labels ("the key insight", "at its core", "TL;DR", "the thing to walk away with").
- No mirror sentences ("A without B, or B without A") and no tidy closers ("the rest follows").
- No flags on a part as important or hard ("here is where it gets interesting"). Just say it.
- The steps in `SKILL.md` are directions to you. Don't echo them as headers or stock phrases.
- Walk through what happens as the person does the thing (opens a long chat, scrolls up) when
  that is what makes it land. Open the diff, the code or the debugger when that is fastest.
