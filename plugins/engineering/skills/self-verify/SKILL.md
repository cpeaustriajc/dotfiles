---
name: self-verify
description: >
  This skill should be used when the user says "set up verification", "verify skill", "agents keep
  claiming done without proof", "we can't review every PR" or "audit the verify skill". It keeps
  the verify skill and per-PR verdict.
---

Most PRs get no human read of the diff. So the agent proves its change with a command a person
can re-run, and a fresh agent checks the proof. Every run reads `references/evidence.md` and the
adapter `references/claude-code.md`. Detail per step: `references/setup.md`.

1. Read the feature files; with none, write one per feature the next change touches.
2. Ask once where and when the full E2E suite runs; never decide it for all projects.
3. Write the verify skill from `references/verify-template.md` into the project: a plugin skill
   does not run before commit.
4. Run it once on one feature: a verify skill never run is a draft. Commit it with the project.
5. On a failed run, fix a wrong feature file or verify skill in the same change. A wrong app is a
   bug, never hidden by editing the map.
6. Weekly audit: `references/weekly-audit.md`. PR verdict: `references/pr-verdict.md`. Green CI
   or a bot approval is no verdict.
7. Each FAIL, and each bug found, ends with one prevention proposal, applied only on the user's
   yes.

Out of scope: a 21-step ship pipeline, an always-on browser daemon, coverage scoring, hourly
audit loops.
