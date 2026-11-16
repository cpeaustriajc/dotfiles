---
name: review-loop
description: >
  This skill should be used after a build or a fix, before its PR is marked ready, and when the
  user says "run the review loop" or "is this ready for review". It runs verify, code review and
  simplify in rounds until a round changes nothing.
---

The thread that built the change runs this loop on its own diff, because it holds the purpose.
An orchestrator does not run it for a thread.

Paths are relative to this skill's folder.

## Setup

When the project has no copy of this skill among its own project skills (the folder where this
harness loads a repo's skills), or its hooks have no `guard_tests.py`, set up first:

1. Find how the project runs verify, review and simplify: its verify skill or script, its code
   review rule, CI config, package scripts, `AGENTS.md` or `CLAUDE.md`.
2. Write a project copy of this skill in that folder: this file without its Setup section, with
   those commands filled in, `scripts/tests_kept.py` beside it, and a description that keeps
   only the triggers the copy serves. Put `# <plugin> <version>`, from the marketplace manifest
   or the version folder in this skill's path, on the line after the opening `---`. Commit it on
   its own, following the project's branch rules and commit hooks, else on a new branch with the
   hooks on.
3. Add the test guard, a hook that asks before an edit rigs a test, where this project's harness
   runs committed project hooks (a cloud session sees only committed ones):
   - Mode: run `python3 -I scripts/replay.py` in the project. `full` if the full rules ask on few
     commits, `rigs` if on many, `off` if the rig rules do too. Report the counts.
   - Copy `scripts/guard_tests.py` and `scripts/tests_kept.py`; write `guard_tests.json` with the
     keys in the script's docstring; wire it in, for example with `scripts/merge_hooks.py` and
     `scripts/guard_tests.settings.json`. Commit the hook on its own.
   - A refused setup edit: skip the guard and report it as not set up.
4. Run the copy from its Loop section, not this file.

Running setup again regenerates the copy and the guard's config; the wiring is left as is.

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
