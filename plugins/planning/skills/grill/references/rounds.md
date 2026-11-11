# Rounds

Read this before the first round of a grill. The steps are in `SKILL.md`.

## Facts

- Sources: code, specs, mockups, the tracker, docs, past transcripts, the live app.
- Look things up yourself, broad searches included. Use read-only subagents only for parallel
  searches too large for your context.
- While a lookup runs, hold only the questions that depend on it; ask the rest now.
- A probe is a short script in the ignored work folder, the vendor's code or the PR state. It is
  not a write. Example: a plan rests on "the client reuses its connections", so a script answers
  that before the round, not after the grill. The final ledger holds no "I assume" item that a
  decision rests on.
- An answer from a spec, a design mockup, a sibling product's pattern or a known convention
  (Auth0- or Clerk-style sign-in) goes under Assumed. So does a question with one obvious
  answer: "Should we show the missing price?" when it is plainly a bug becomes "fix it".

## The ledger

Post it in chat, before the form:

```
**Settled:** postgres · API v2 only (v1 is gone) · mobile out of scope
**Assumed (veto any):** auth follows the partner's spec · fix missing price, it's a bug
**Out of scope (veto any):** SSO for guests: no guest accounts exist (checked the users table)
**Open after this round:** 6
```

Every constraint I state goes into Settled. Every cut under Out of scope carries a reason you
checked. A part of the source I named (a repo to port, a
list I pasted) is a question, not a cut.

## Asking

- One ask-tool call per round, with as many questions as it takes (up to the
  tool's limit). A numbered list in chat is not a form.
- The recommended option comes first, marked "(Recommended)". Each option gets a one-line
  consequence: what it costs, touches or locks in. Justification stays in the options.
- Each question carries a concrete scenario: "A visitor types 'home security' and gets no
  results. A shows…, B shows…".
- Plain words: no section numbers, internal IDs, letter codes or unexplained jargon. Define a
  term I may not know in half a line.
- A layout, look or feel question shows each option as a mockup, or offers "show me a mockup
  first". A flow, state change or structure (a pipeline, a state machine, a module layout)
  comes as a diagram, in a question or in the final ledger.
- A decision that touches other people (PO, QA, another team) is worded as they would read it:
  neutral, no blame, no work implied as theirs unless I said so.
- Done is recommended from what you looked up. Asking "what are the success criteria?" hands
  your job back to me.

## Reading my answers

- **A note or "Other"** usually reframes the question or adds a requirement. Fold it into the
  tree and recompute the frontier; the original question is not re-asked as it was.
- **A counter-question** ("what's base_url again?") means I lacked context. Answer in 1-2
  lines, then ask the question again next round.
- **"Up to you" or "not sure"**: log your recommendation under Assumed. **"You research it"**:
  look it up and treat the result as a fact.
- **A skipped or partial answer** leaves that question open. **"Handle Q1 first"** reorders
  the rounds.
- **A dismissed or rejected form** means stop and follow what I type next. The same form is
  never sent again.
- **Bulk replies** ("yes to all", "1 yes, 2 the second one") settle everything they name.
