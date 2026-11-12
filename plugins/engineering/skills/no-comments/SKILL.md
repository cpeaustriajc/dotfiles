---
name: no-comments
description: "This skill should be used when the user types /no-comments with a folder of old code: spawn the sweeper, fix accepted findings, land comment deletions, suppression removals and reshapes as separate commits with the same test results, offer encodings for claimed constraints, and hand each MUST KILL to /architect."
disable-model-invocation: true
argument-hint: "<folder>"
---

Scope: every tracked source file below `$ARGUMENTS`; else the caller's files or diff; else the
diff against the base branch (default `main`) with the working tree. The sweeper finds; this
session judges and lands. Detail per step: `references/steps.md`. Adapter:
`references/claude-code.md`.

1. **Prepare.** Uncommitted work: stop for the owner. Save the baseline:
   each exit code and failing check of the typecheck, lint and tests.
2. **Sweep** with a read-only sweeper and `references/sweeper-prompt.md`. Defer to its fresh
   perspective.
3. **Review** its report. A second rejected report fails `/no-comments`.
4. **Constraints**: `references/constraints.md`. Delete none before its claim is refuted.
5. **Land** on a branch as up to three commits of one kind each: Comments, Reshapes,
   Suppressions. After each change the baseline must hold; else undo that item and report it
   open. Never commit a changed result. Skip an empty commit.
6. **Report** per `references/report.md`, then the inline view. With a constraint offer, wait.
7. Act on the owner's reply per `references/constraints.md`.

## Credit

Adapted from pstack's `no-comments` and its comment agent by Lauren Tan (MIT; see `LICENSE`).
