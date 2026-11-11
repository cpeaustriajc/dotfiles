# Report

Step 6 (Report) of `SKILL.md`.

1. The deletion count: comments and suppressions together, the same number everywhere in the
   report.
2. Each `MUST KILL` flag in one line: `file:line symbol: reason`.
3. Skips, each with its reason.
4. The commits with their before and after results, restored comments, reruns, fixes, encoding
   offers, unproven and unenforced constraints, and other open work.

An empty sweep reports `0 deletions in <folder>` and the number of files read, and makes no
commit.

Then the inline view, built as the adapter says. Its `file:line` values are the lines after the
commits of step 5, not the sweeper's lines.

- Each `MUST KILL`: the deleted comment beside the code it excused, its reshape line, its commit
  if a reshape fixed it, and one action that sends it to `/architect`. The action's task names
  the logic re-architecture: the symbol, its file, the reshape and the deleted comment.
  `/architect` stops at its sketches.
- Each proven constraint: its comment beside its code, the evidence, and the offered encoding,
  with an Encode and a Delete action.
