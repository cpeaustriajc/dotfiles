# Rounds

Read this before the first round of a grill. The steps are in `SKILL.md`.

## Facts

- Sources: code, specs, mockups, the tracker, docs, past transcripts, the live app.
- Read-only subagents only for parallel searches too large for your context. While a lookup
  runs, ask the questions that do not depend on it.
- A probe is a spike, not a write: a short script in the ignored scratchpad, the vendor's code or
  the PR state. The final ledger holds no "I assume" item that a decision rests on.
- An answer from a spec, a mockup, a sibling product or a known convention goes under Assumed,
  and so does a question with one obvious answer ("Should we show the missing price?" becomes
  "fix it").

## The ledger

Post it in chat, before the form:

```
**Settled:** postgres · API v2 only (v1 is gone) · mobile out of scope
**Assumed (veto any):** auth follows the partner's spec · fix missing price, it's a bug
**Out of scope (veto any):** SSO for guests: no guest accounts exist (checked the users table)
**Open after this round:** 6
```

Every constraint I state goes into Settled. Every cut under Out of scope carries a reason you
checked. A part of the source I named (a repo to port, a list I pasted) is a question, not a cut.

## Asking

- One ask-tool call per round; a numbered list in chat is not a form.
- The recommended option comes first, marked "(Recommended)", each option with a one-line
  consequence. Each question carries a concrete scenario.
- Plain words: no section numbers, internal IDs or letter codes.
- A layout, look or feel question shows each option as a mockup, or offers "show me a mockup
  first". A flow, state change or structure comes as a diagram.
- A decision that touches other people (PO, QA, another team) is worded blamelessly, as they
  would read it.
- Done is recommended from what you looked up; "what are the success criteria?" hands your job
  back to me.

## Reading my answers

- **A note or "Other"** reframes the question or adds a requirement: fold it into the tree and
  recompute the frontier. **A counter-question** means I lacked context: answer in 1-2 lines,
  then ask again next round.
- **"Up to you" or "not sure"**: log your recommendation under Assumed. **"You research it"**:
  look it up and treat the result as a fact.
- **A skipped or partial answer** leaves that question open. **"Handle Q1 first"** reorders.
- **A dismissed or rejected form** means stop and follow what I type next; never resend it.
- **Bulk replies** ("yes to all", "1 yes, 2 the second one") settle everything they name.
