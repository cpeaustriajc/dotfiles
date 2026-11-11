# Gate, questions, build and PR body

Steps 3, 4, 5 and 7 of `SKILL.md`. A criterion is one line of the ticket that says when the work is
done; use the project's own name for it in everything you write.

## Gate (step 3)

Check each line. If one fails, stop and name it.

1. The item is `ready-for-agent` (or the team's name for it). Any other state: run `triage`.
   At `ready-for-human`, build only the part an agent can prove and put the rest under Needs
   you.
2. It has criteria, each a check that passes or fails.
3. Every item that blocks it is closed, or has a pushed branch with an open PR. Without the
   second case, a stack never builds past its first item.

Then start from the branch of the ticket's blocker while its PR is open, else a fresh trunk (as
the `playbooks` feature playbook says). Skip this only if the current branch is already for this
item. Never build on the trunk.

## Open questions (step 4)

Do not run `grill`. Do not propose a different approach. For each question the ticket does not
answer:

| The answer is | Do |
|---|---|
| Easy to undo | Follow the closest existing pattern. Add it to Decided. |
| Costly to undo, or against the spec or a recorded decision | Stop. Post triage notes on the item, move it to `needs-info`, report. |

A criterion that cannot be met as written is a costly question.

## Build (step 5)

1. Run the feature playbook (`playbooks`, `references/feature.md`) from step 2 to step 6. The
   ticket settled step 1; step 7 here opens the PR, after the review. A bug item runs the bug
   playbook instead, up to its report.
2. Save each check's command and evidence. Never commit red.
3. Put a side discovery in the report, not in the change.

## Review (step 6)

Fix each Act on row in its own commit, and rerun the checks it touches.

## PR body (step 7)

1. The tracker's close word or link for the item, so the merge closes it. Never close it by
   hand.
2. One row per criterion: the criterion, the command, the evidence path, and VERIFIED, NOT
   VERIFIED or INCONCLUSIVE. INCONCLUSIVE is not a pass.
3. **Decided:** each answer from step 4 that the ticket did not give.
4. **Needs you:** each line only a person can check.
