---
name: review-loop
description: >
  This skill should be used after a build or a fix, before its PR is marked ready, and when the
  user says "run the review loop" or "is this ready for review". It runs verify, code review and
  simplify in rounds until a round changes nothing.
---

The thread that built the change runs this loop on its own diff, because it holds the purpose.
An orchestrator does not run it for a thread.

## Setup

When the project has no copy of this skill among its own project skills (the folder where this
harness loads a repo's skills), set up first:

1. Find how the project runs verify, review and simplify: its verify skill or script, its code
   review rule, CI config, package scripts, `AGENTS.md` or `CLAUDE.md`.
2. Write a project copy of this skill in that folder with those commands filled in and no Setup
   section, and copy `scripts/tests_kept.py` beside it. Stamp this skill's version or commit in
   the copy's front matter or first line.
3. Run the copy, not this file.

Running setup again regenerates the copy.

## Loop

One round, in order:

1. Run the project's verify check for the change's issue. With none, the step is BLOCKED: say so
   in the report. Tests: `references/tests.md`.
2. Run `python3 -I scripts/tests_kept.py --base <base>`. Each line it prints is a finding a user
   would hit; exit 2 is BLOCKED.
3. Run the project's code review of the diff. Give it the issue's acceptance lines and the project's users as
   the purpose.
4. Fix each finding that a user would hit. Handle each other finding as the project's review
   rule says; with no rule, list it in the report.
5. Run the project's simplify pass on the diff and apply its fixes.

Repeat to a fixed point: stop after a round, run after the last change, where verify and
`tests_kept.py` pass, the review finds nothing a user would hit, and no step changed the code.

Report the last round: the verify and `tests_kept.py` lines as printed, the review result, and each
finding that is not fixed.
