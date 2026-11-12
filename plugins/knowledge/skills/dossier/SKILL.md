---
name: dossier
description: >
  This skill should be used when the user says "note that down as a decision", "what did we decide
  about X" or "supersede that decision". It keeps the project's dossier: decision and research
  pages in the team's wiki or Notion. Agent rules: CLAUDE.md.
---

Decision log and research pages live where the team writes, never in the code repo, and are
written for people; agent instructions go in `CLAUDE.md`.

1. Find the log in the order of `references/locate.md`.
2. Read the backend's adapter in `references/`: `github-wiki.md`, `notion.md`, `linear.md`,
   `obsidian.md` or `other-backends.md`. Then read `references/shape.md`. Before the first write,
   learn the log's own conventions; they win over the adapter, and the adapter over `shape.md`.
3. "What did we decide about X": read every match in full and follow each "Superseded by" and
   "Partly superseded by" chain to its end. Report the current decision (or the part that
   stands), then what it replaced, with dates and page names. The chain is the authority, not
   the latest commit. No match: say so; code and memory are not the record. Before a code
   change, end with Preserve, Change, Avoid, Risk.
4. Record, supersede, file research or move rationale: `references/operations.md`. A decision
   page is never rewritten; only its Status line changes. A missing reason reads "not
   recorded" and you ask me: an invented one props up every later decision.
5. Publish per `references/publish.md`: I see the first write to a shared space, and every page
   passes its checks and `references/plain-prose.md`. Save after every change.
