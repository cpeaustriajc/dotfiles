---
name: refine
description: >
  This skill should be used when the user says "refine these tickets", "anything still
  unanswered?", "is this ready for an agent", "keep refining until nothing is unclear" or
  "fact-check the drafts", after tickets drafts a set and before triage marks one ready. It loops
  drafts through fact probes and cold reads.
---

Treat each open question as a fact you have not checked yet. You find the facts; I make the
calls only I can make and approve the tracker writes. Commands: `references/claude-code.md`.

1. Version the drafts in a private draft space: the harness's document or artifact tool, or else
   a session temp directory outside the repo. Treat the tracker as read-only until I approve.
2. Read the trunk, the contract, the ticket threads and the decision log in full; search meeting
   notes and mail for the tickets' terms. Quote my settled answers with their date; never ask again.
3. List the gaps that would stop a builder or QA: edge cases, race conditions, stale state,
   chained cases, limits and checks nobody can run. Leave wording to the cold read.
4. Spike each gap before you ask me. Fan the spikes out read-only, each on the cheapest model
   that can answer. Ask my go for a spike with side effects, and hand me any sign-in, payment or
   secret. Work outside the tickets' scope, such as another ticket set, a research question or an
   environment probe, goes to its own session; bring back only its conclusion.
5. Write draft n+1 to a Definition of Ready. Give each choice a confidence and evidence: a
   permalink, or a command and its output. Make each check testable, with its owner, fixture and
   environment. Add missing setup as a check on the same ticket.
6. Start a cold read per `references/cold-read.md`: a fresh-context reviewer reads the first
   draft in full and blind, and each later round re-checks only the last fixes.
7. Triage its findings into a decision log beside the draft. A finding only I or an outside party
   can settle goes to the residual risks once and blocks nothing. Delegate the drafts and the
   edits to a cheaper agent, and keep the orchestration yourself.
8. Repeat steps 4 to 7 for the new blockers until a read finds none. Slips alone never start
   another round.

Then report the rounds and their finding counts, each choice with its confidence and the
alternative, the steps only a person can do, and the residual risks. Send a security issue to me
privately. After I approve, `tickets` writes the items and `triage` sets their states.
