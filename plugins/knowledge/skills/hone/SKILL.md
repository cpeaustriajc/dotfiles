---
name: hone
description: >
  This skill should be used when the user says "hone", "what do I keep correcting", "reflect" or
  "learn from my sessions", or asks why the agent keeps doing X. It mines transcripts for repeated
  corrections. Not for one instruction-file edit.
---

A correction I made twice is a missing mechanism: propose its cheapest durable fix. Code-host commands: `references/github.md`.

1. Gather from each source in `references/sources.md`, the lens pass included. Brief each miner
   with `references/miners.md`.
2. Keep a lesson only if it recurs (2+ sessions, or once with an obvious cost) and the agent would
   repeat it unchanged. A one-off preference, an enforced fact or a single-run correction goes
   under Rejected. A rule broken anyway needs a stronger layer, not a copy.
3. Prune: the harness's instruction-file audit (find its command; it reports and edits nothing,
   and for an installed skill audit the skill's source path), stale commands and paths, lines that changed nothing, repeated wasted tool
   calls, unwired checks. An always-loaded file over 200 lines loses adherence. A real rule in the wrong file moves, never drops.
4. Route each lesson to the strongest layer that holds it: `references/layers.md`. A proposed
   lint, test or hook starts red on a real past instance, or it stays out.
5. Propose, then stop: **Accept?** (quotes, session count, layer, why each stronger layer
   fails, the diff with its removed lines), **Backlog** (needs real work), **Rejected** (one-line
   why).
6. Ask which to apply with the harness's ask tool, one multi-select option per proposal; apply only those. A skill fix: its own PR, in its
   source repo, since an update overwrites the installed copy. A file a config manager owns:
   change its source, then commit.
