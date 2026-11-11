# PR title, body and metadata

Title in commit style. Body: the repo's template, else its recent merged PRs' form, else:

```
<1-3 lines: what changed and why, for a reviewer who hasn't seen the issue>

Evidence: <before and after of one state, and the re-run command>
Merge danger: <one-way or two-way door; blast radius>
Test changes: <each changed or removed test line and why, or "additions only">
```

- No headings, checklists or test-plan sections unless the template asks. Keep it short.
- Visual only when it replaces prose: the smallest one, after the line it supports, in this
  order of preference: a `diff`, a tree, pseudocode, Mermaid for a changed flow. A typo or
  one-line fix gets none.
- Evidence: a visual change, flow or timing follows `evidence.md`; else the test red before, green
  after. No E2E run: no line.
- Merge danger: `one-way door, adds premium_prices table; blast radius: search and checkout totals.`
- Test changes: `notify.test.ts toHaveBeenCalledTimes(1) to (2), the digest now sends twice.`
- Metadata goes in the code host's fields, not the body: reviewers, labels, assignee, milestone,
  project. Find the issue in the branch name, the commits or the session, and put its key in the branch
  name or title, so the tracker links the PR.
  A closing keyword (`Closes`, `Fixes`) closes the issue on merge, before the verifier passes it.
