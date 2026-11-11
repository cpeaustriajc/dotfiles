---
name: grill
description: >
  This skill should be used when the user says "grill me", "ask me questions first", "stress-test
  this", "poke holes in this" or "plan and ask me" about a change. A product idea, or whether it
  is worth building, goes to vision.
---

Facts are your job, decisions are mine. Tools: `references/claude-code.md`.

1. Look the work up; name its size in one line (I can change it):
   - trivial (1-2 files, one obvious approach): your plan, then "go?";
   - small (one decision): ask it, then stop;
   - grill (3+ files, several approaches, unclear scope, new architecture, others see it):
     rounds per `references/rounds.md`.
2. Map a design tree. Each round asks the frontier, most-unblocking first.
3. Look up facts before asking; probe any a recommendation rests on ("research first" is no
   option). Known or obvious answers go under Assumed.
4. Open each round with the ledger. Settled starts from the parent product or spec; a Settled
   item is never re-asked or contradicted, and evidence against one gets one conflict question.
5. Round 1 settles done as an observation: who does what, what they see.
6. Recommend the smallest version that ships and costs least to run; cut gold-plating; flag
   scope drift in one line.
7. Write nothing (code, tracker, docs, pushes). Frontier empty: post the final ledger and ask
   if we share an understanding; on yes, offer `shape`, `tickets` or `project-knowledge`, then
   wait.
