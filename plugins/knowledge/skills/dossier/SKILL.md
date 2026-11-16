---
name: dossier
description: >
  This skill should be used when the user says "note that down as a decision", "what did we decide
  about X", "supersede that decision", "record this research" or "set up this project". It keeps
  the project's dossier: decision and research pages in the team's wiki or Notion, and what a
  long session needs after compaction. Agent rules: the instruction file.
---

Decision log and research pages live where the team writes, not in the code repo (an existing
`docs/adr/` is followed: `references/shape.md`), and are written for people; agent instructions go in the project's instruction file (`AGENTS.md`, `CLAUDE.md` or the harness's own).

1. Find the log in the order of `references/locate.md`. When the project has no copy of this
   skill among its own project skills (the folder where this harness loads a repo's skills), or
   I say "set up this project", set up first, then run the copy, not this file:
   - Find what reaches the backend: the connected tools' lists, the CLI's `--help`, a folder of
     files. Read its page and link rules, and the log's newest pages.
   - Write the copy there with no Setup step, and `references/` and `scripts/` beside it. Add a
     Backend section: which tool serves find, read, record, supersede and link; where Home, the
     decision log and the research pages sit; the page-name and link rules; how a save happens.
     Stamp this skill's version or commit in the copy's first line.
   - Write and commit the pieces of `references/long-session.md`, on their own.
   - A backend with no create or update tool: hand me the page text to paste; never fake a write
     through an issue or a comment. A backend of an unknown kind: say which tool serves each
     operation and how a superseded decision is marked, and get my yes before writing.
2. Read the backend section of the project's copy of this skill (Setup), then
   `references/shape.md`. Before the first write, learn the log's own conventions; they win over
   the backend section, and it over `shape.md`.
3. "What did we decide about X": read every match in full and follow each "Superseded by" and
   "Partly superseded by" chain to its end. Report the current decision (or the part that
   stands), then what it replaced, with dates and page names. The chain is the authority, not
   the latest commit. No match: say so; code and memory are not the record. Before a code
   change, end with Preserve, Change, Avoid, Risk.
4. Record, supersede, file research or move rationale: `references/operations.md`. A decision
   page is never rewritten; only its Status line changes. A missing reason reads "not
   recorded" and you ask me: an invented one props up every later decision.
5. Publish per `references/publish.md`: I see the first write to a shared space, and every page
   passes its checks and `references/plain-prose.md`. Save after every change. Where a save
   reaches others at once (a synced folder, a hosted workspace, a wiki), saving is publishing.
   A backend with its own editor can conflict: show me both versions, and never force-push.
