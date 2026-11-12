# Table, verdict and sign-off

Steps 4 and 5 of `SKILL.md`. One table, one row per issue, most visible first:

| # | Where | Before | After | Why |
|---|---|---|---|---|

- "Where": screen location, and `file:line` when in code. "Why" names the rule broken. Attach a
  screenshot when the issue is visual.

Then one verdict: **Ship**, **Ship after the top N**, or **Rework** when off-design.

A pass counts only with its table and verdict. For a visual change, put before and after screenshots
in the PR body; the PR review is the sign-off. Wait before committing only when the project requires
it or the commit goes to the trunk.
