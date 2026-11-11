---
name: why
description: >
  This skill should be used when the user asks "why is this code like this", "where did this
  number come from", "can I delete this guard" or "what's the history behind this". It digs
  through git, PRs and docs, and labels evidence.
---

The answer is the evidence for the code's shape, each claim labelled. A plausible reason nobody
wrote down is not an answer.

1. **Target and question**; if I was vague, say your guess. Read only the decision log's
   index and decision pages, as `project-knowledge` says (research and specs are step 3's docs):
   evidence, not the end. A reason my question assumes is one candidate.
2. **Seed anchor**, in this session, per `references/git.md`: lines, symbols, the commits that
   last touched and first added them, PR and ticket IDs. Defensive code (a null check, retry,
   timeout, cap, flag) adds a search for its incident.
3. **Sources**: list each as available, or unavailable with the reason. Git always; PRs with
   a remote and sign-in; tracker and docs when a tool reaches them. Only git: sweep it yourself.
   Two or more: before you read them, one read-only investigator per source (git and PRs are
   one) in parallel, with `references/investigator.md` (mechanics: `references/claude-code.md`).
   They quote; you synthesize, never hand that on.
4. **Label** every claim per `references/evidence.md`.
5. **Answer** in the chat, in the sections of `references/evidence.md`.
