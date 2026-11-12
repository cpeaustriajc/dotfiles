---
name: review-loop
description: >
  This skill should be used after a build or a fix, before its PR is marked ready, and when the
  user says "run the review loop" or "is this ready for review". It runs verify, code review and
  simplify in rounds until a round changes nothing.
---

The thread that built the change runs this loop on its own diff, because it holds the purpose.
An orchestrator does not run it for a thread. Commands: `references/claude-code.md`.

One round, in order:

1. Run the project's verify skill for the change's issue. Tests: `references/tests.md`.
2. Run `python3 -I scripts/tests_kept.py --base <base>`. Each line it prints is a finding a user
   would hit; exit 2 is BLOCKED.
3. Run a code review of the diff. Give it the issue's acceptance lines and the project's users as
   the purpose.
4. Fix each finding that a user would hit. Handle each other finding as the project's review
   rule says; with no rule, list it in the report.
5. Run a simplify pass on the diff and apply its fixes.

Repeat to a fixed point: stop after a round, run after the last change, where verify and
`tests_kept.py` pass, the review finds nothing a user would hit, and no step changed the code.

Report the last round: the verify and `tests_kept.py` lines as printed, the review result, and each
finding that is not fixed.
