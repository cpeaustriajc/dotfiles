# Steps

The detail behind steps 1, 3 and 5 of `SKILL.md`.

## Prepare (step 1)

- If git doesn't ignore the project's work folder, add it to `.git/info/exclude`. Never edit
  `.gitignore`: a sweep commits only in-scope files, so that edit stays behind and stops the next
  sweep.
- Take the typecheck, lint and test commands from the repo's README, package scripts or
  instructions. Save the baseline to the work folder.

## Review the sweeper's report (step 3)

Don't restate the sweeper's rules in its prompt.


- Reject application-code edits, scope escapes, deletions an exception protects, misstated
  `MUST KILL` reasons, and flags that treat kept intentional code as guilty.
- Reshape flags on surprises in our own code stay actionable. Do not restore those comments.
- A keep survives only with proof that it is about something we cannot change.
- Audit missed scoped lint and TypeScript suppressions. A suppression of a correctness or safety
  rule stays an actionable `MUST KILL`.
- Restore a deletion only with an exact exception and scoped proof. An ambiguous kill stays
  deleted.

## Reshapes

Fix trivial accepted `MUST KILL` flags directly: delete a dead path, drop a parameter that no
caller passes (search the whole repo, not only the folder), or use the real API. Make the
smallest root-cause fix in scope and remove every named workaround; a symptom guard leaves the
flag open. A flag that needs a new shape gets no edit: report it open for `/architect`, which
shapes; this run builds no shape.

## Land (step 5)

- From the trunk, branch by the repo's branch rule, else `no-comments/<folder>`.
- Commit in this order, one kind per commit, staging only in-scope files you changed and never
  the work folder:
  1. **Comments**: delete each accepted comment. Change no code token.
  2. **Reshapes**: per Reshapes above.
  3. **Suppressions**: delete each accepted suppression.
- "The baseline holds" means the same exit codes and the same failing checks. When a result
  changes, undo the item that changed it, report it open with the check that changed, and run
  the checks again before the commit.
- A rejected sweeper report gets one rerun with the failure named; a second rejection is reported
  open.

