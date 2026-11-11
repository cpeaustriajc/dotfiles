---
name: drive
description: >
  This skill should be used when the user says "drive this", "loop until it passes", "keep going
  until green", "run it overnight" or "hillclimb", hands over a ticket to finish unattended, or
  before writing a goal or Stop hook. It decides whether the work should loop, writes the exit
  check first, freezes the harness, then makes one change per pass, kept or reverted, with a log
  on disk and a brake on lack of progress. Not for a timer; that is /loop.
---

Adapter: `references/claude-code.md`. Detail: `references/run-files.md`.

1. Loop only with a check free of judgement, a harness that reproduces the problem now, and
   undoable actions (deploys, deletes, payments, messages wait for me). Taste, design and
   one-turn work get one turn or a playbook.
2. Show me the exit check first. A wrong predicate stops the run: relaxing it fakes a win.
3. Baseline untouched code; a deliberate break must turn it red. Then freeze it.
4. Each pass, from disk: one hypothesis, the smallest change, pasted check output; then commit
   or revert. Stacked untested changes hide the breaker.
5. Brake on progress, not turns: stuck, change the kind of hypothesis once, then stop. Also stop
   at budget or a Holds throughout conflict.
6. For a run that matters, a fresh reviewer confirms done: self-graders declare victory early.
7. A fresh agent audits the log (`references/audit.md`).
8. Report the Attention list first: verdict-first replies buried it in 4 of 18 eval runs.
