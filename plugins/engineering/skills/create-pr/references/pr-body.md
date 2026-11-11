# PR title and body

Title in commit style. Body: the repo's template, else its recent merged PRs' form, else:

```
<1-3 lines: what changed and why, for a reviewer who hasn't seen the issue>

Related: <issue>
Evidence: <before and after of one state, and the re-run command>
Merge danger: <one-way or two-way door; blast radius>
Test changes: <each changed or removed test line and why, or "additions only">
```

- Visual only when it replaces prose: a `diff`, tree, pseudocode or Mermaid.
- Evidence: a visual change, flow or timing follows `evidence.md`; else the test red before, green
  after. No E2E run: no line.
- Merge danger: `one-way door, adds premium_prices table; blast radius: search and checkout totals.`
- Test changes: `notify.test.ts toHaveBeenCalledTimes(1) to (2), the digest now sends twice.`
- `Related:` only. `Closes` closes the issue on merge, before the verifier passes it. No issue: no
  line.
