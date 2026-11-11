---
name: interrogate
description: >
  This skill should be used when the user says "interrogate", "second opinion" or "cross-check
  this", or before a PR on a risky change (auth, money, migrations, concurrency). Fresh reviewers
  each check one slice of the diff.
---

Reviewers that never saw the author's story catch what it explains away. Commands:
`references/claude-code.md`.

1. **Bundle**: the diff I named (PR, branch, range), else the branch against its base, else
   uncommitted changes. Add each changed file with its own line numbers, the spec if one
   exists, and one paragraph on what the change should do.
2. **Reviewers**: Full, Blind and Spec per `references/review.md`, read-only, with fresh
   context, in parallel.
3. **Judge**: verify each finding against the code yourself and sort it into Act on, Consider,
   Noted or Dismissed per `references/review.md`. Agreement counts little.
4. **Report** the groups as tables: reviewers, file:line, proof level, failure scenario. Apply
   nothing until I pick. Save the bundle and raw reviews in the ignored work folder; say where.
5. **Quality pass**, only when I ask: after my picked fixes, a fresh reviewer reads the diff for
   reuse, quality and efficiency. Its changes stay uncommitted.
