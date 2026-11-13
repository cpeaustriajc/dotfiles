---
name: refine
description: >
  This skill should be used when the user says "refine these tickets", "anything still
  unanswered?", "is this ready for an agent", "keep refining until nothing is unclear" or
  "fact-check the drafts", after tickets drafts a set and before triage marks one ready. It loops
  drafts through fact probes and cold reads.
---

Treat each open question as a fact you have not checked yet. You find the facts; I make the
decisions and approve the writes. Commands: `references/claude-code.md`.

1. Version the drafts in a private draft space: the harness's document or artifact tool, or else
   a session temp directory outside the repo. Treat the tracker as read-only until I approve.
2. Read every source of truth in full: the trunk, the contract, the ticket threads, the decision
   log and the meeting notes. Quote my settled answers with their date, and do not ask them again.
3. Write a gap list. Look for edge cases, race conditions, stale state, chained cases, limits and
   checks nobody can run.
4. Spike each gap before you ask me. Fan the spikes out read-only, each on the cheapest model
   that can answer. Ask my go for a spike with side effects, and hand me any sign-in, payment or
   secret.
5. Write draft n+1 to a Definition of Ready. Give each choice a confidence and evidence: a
   permalink, or a command and its output. Make each check testable, with its owner, fixture and
   environment. Add missing setup as a check on the same ticket.
6. Start a cold read: a fresh-context reviewer that has not seen your reasoning reads the draft,
   per `references/cold-read.md`.
7. Triage its findings into a decision log beside the draft. Delegate the edits to a cheaper
   agent, and keep the orchestration yourself.
8. Repeat from step 3 until you reach a fixed point: a cold read that finds no blockers, only
   slips it fixed itself.

Then report the rounds and their finding counts, each choice with its confidence and the
alternative, the steps only a person can do, and the residual risks. Send a security issue to me
privately. After I approve, `tickets` writes the items and `triage` sets their states.
