---
name: bug-hunt
description: >
  This skill should be used when the user says "bug hunt", "deep code review", "audit the
  codebase", "hunt for bugs until clean" or "find and fix every bug". Hunters fix bugs test-first,
  until a clean round. One diff: interrogate.
---

One pass hides bugs behind the ones it finds, and each fix changes what the next pass reads, so
repeat until a round is clean. A periodic sweep; one change's proof is `self-verify`. Commands
and the work folder: `references/claude-code.md`.

1. **Scope**: what I named, else the repo minus generated, vendored and lock files. Write the
   file list to the ignored work folder and split it into three shards of about equal lines,
   one area each. Read the test and E2E commands and the rules on test ids and copy.
2. **Round**: three hunters in parallel with `references/hunter-brief.md`. Each reads the
   whole scope and edits only its shard, so no two edit one file. Rotate shards each round.
3. **Between rounds**: coverage, verify, route, ledger, prevention, suite, commit, per
   `references/rounds.md`.
4. **Stop** when all three report `BUGS FOUND: 0` at 100% coverage. Ask me after 5 rounds, or
   when a round finds only rejected bugs. Report per `references/rounds.md`.
