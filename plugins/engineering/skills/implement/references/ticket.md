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

Then branch per `../../create-pr/references/stacking.md`, unless the current branch is already for
this item.

## Open questions (step 4)

Do not run `grill`. Do not propose a different approach. For each question the ticket does not
answer:

| The answer is | Do |
|---|---|
| A two-way door | Follow the closest existing pattern. Add it to Decided. |
| A one-way door, or against the spec or a recorded decision | Stop. Post triage notes on the item, move it to `needs-info`, report. |

A criterion that cannot be met as written, or a test that contradicts the spec, is a one-way door.

## Build (step 5)

Cut the work into vertical slices that each end in a state you can check in the running app. Per
slice: write its test per `../../review-loop/references/tests.md`, see it fail, build, see it pass,
commit. Never commit red.

## PR body (step 7)

1. The item's key as a link; `create-pr` rejects a closing keyword.
2. One row per criterion: the criterion and the verify skill's line for it as printed, with its
   log path. Any result but a pass is not a pass.
3. **Decided:** each answer from step 4 that the ticket did not give.
4. **Needs you:** each line only a person can check.
