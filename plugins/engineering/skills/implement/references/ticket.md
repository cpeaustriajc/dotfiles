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

Then start from the branch of the ticket's blocker while its PR is open, else a fresh trunk. Skip this only if the current branch is already for this
item. Never build on the trunk.

## Open questions (step 4)

Do not run `grill`. Do not propose a different approach. For each question the ticket does not
answer:

| The answer is | Do |
|---|---|
| A two-way door | Follow the closest existing pattern. Add it to Decided. |
| A one-way door, or against the spec or a recorded decision | Stop. Post triage notes on the item, move it to `needs-info`, report. |

A criterion that cannot be met as written is a one-way door.

## Build (step 5)

1. Follow the spec, the design and the closest existing pattern in the app. Cut the work into
   vertical slices that each end in a state you can check in the running app. Per slice: build it, run
   its end-to-end check, commit. Take each expected value from the spec, never from the code.
   A bug item goes red-green: a failing end-to-end check reproduces the bug first, then the fix of its cause turns it green.
2. Save each check's command and evidence. Never commit red.
3. Put a side discovery in the report, not in the change.

## Review (step 6)

Commit each `review-loop` fix on its own, and rerun the checks it touches.

## PR body (step 7)

1. The item's key as a link, not a closing keyword: the verifier closes the item once it passes.
2. One row per criterion: the criterion, the command, the evidence path, and VERIFIED, NOT
   VERIFIED or INCONCLUSIVE. INCONCLUSIVE is not a pass.
3. **Decided:** each answer from step 4 that the ticket did not give.
4. **Needs you:** each line only a person can check.
