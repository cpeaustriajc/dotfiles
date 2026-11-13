---
name: refine
description: >
  This skill should be used when the user says "refine these tickets", "anything still
  unanswered?", "is this ready for an agent", "keep refining until nothing is unclear" or
  "fact-check the drafts", after tickets drafts a set and before triage marks one ready. It loops
  drafts through fact probes and cold reads.
---

Treat each open question as a fact you have not checked yet. You find the facts; I make the
calls only I can make and approve the tracker writes. Ask me with the harness's ask tool, each option with its confidence.

1. Version the drafts in a private draft space: the harness's document or artifact tool, or else
   a session temp directory outside the repo (`draft-<n>.md`, `review-<n>.md`, `decisions-<n>.md`). Treat the tracker as read-only until I approve.
2. Read the trunk, the contract, the ticket threads and the decision log in full; search meeting
   notes and mail for the tickets' terms. Quote my settled answers with their date; never ask again.
3. List the gaps that would stop a builder or QA: edge cases, race conditions, stale state,
   chained cases, limits and checks nobody can run. Leave wording to the cold read.
4. Spike each gap before you ask me. Fan the spikes out read-only, each on the cheapest model
   that can answer (a code or file lookup needs less than the tracker, the web or a browser run). Ask my go for a spike with side effects, and hand me any sign-in, payment or
   secret. Work outside the tickets' scope, such as another ticket set, a research question or an
   environment probe, goes to its own session; bring back only its conclusion.
5. Write draft n+1 to a Definition of Ready. Give each choice a confidence and evidence: a
   permalink, or a command and its output. Make each check testable, with its owner, fixture and
   environment. Add missing setup as a check on the same ticket.
6. Start a cold read per `references/cold-read.md`: a fresh-context reviewer on the strongest
   model reads the first draft in full and blind, and a mid-tier one re-checks only the last
   fixes each later round.
7. Triage its findings into a decision log beside the draft. A finding only I or an outside party
   can settle is a risk: log it once with its owner, likelihood, impact and a mitigation in the
   draft (a fallback, a check, a flag) or an accept, then stop working it. Delegate the drafts and the
   edits to a mid-tier agent with the decision log, and keep the orchestration yourself.
8. Repeat steps 4 to 7 for the new blockers until a read finds none. When the harness has a
   completion check, run the loop under it with: "the last re-check found 0 blockers, and every
   open item is in the risk log with a mitigation or an accept". Slips alone never start
   another round. A long session keeps the round, the open decisions and the spikes run in one
place I can open.

Then report the rounds and their finding counts, each choice with its confidence and the
alternative, the steps only a person can do, and the risk log. Send a security issue to me
privately. After I approve, `tickets` writes the items and `triage` sets their states.
