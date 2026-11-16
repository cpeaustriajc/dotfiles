---
name: dossier
description: >
  This skill should be used when the user says "note that down as a decision", "what did we decide
  about X", "supersede that decision" or "record this research". It keeps the project's dossier:
  decision and research pages in the team's wiki or Notion. Agent rules: the instruction file.
---

Decision log and research pages live where the team writes, not in the code repo (an existing
`docs/adr/` is followed: `references/shape.md`), and are written for people; agent instructions go in the project's instruction file (`AGENTS.md`, `CLAUDE.md` or the harness's own).

1. Find the log in the order of `references/locate.md`. When the project has no copy of this
   skill among its own project skills (the folder where this harness loads a repo's skills), set
   up first, then run the copy from its step 2, not this file:
   - Find what reaches the backend: the connected tools' lists, the CLI's `--help`, a folder of
     files. Read its page and link rules, and the log's newest pages.
   - Write the copy there: this file without these Setup bullets, the files its other
     steps name and the files those use (one outside this skill's folder goes into the copy's folder,
     with its path rewritten), and a description that keeps only the triggers the copy serves. Add a Backend section: which tool serves find, read, record, supersede and
     link; where Home, the decision log and the research pages sit; the page-name and link
     rules; how a save happens. Put `# <plugin> <version>`, from the marketplace manifest or the
     version folder in this skill's path, on the line after the opening `---`. Commit it on its
     own, following the project's branch rules and commit hooks, else on a new branch with the
     hooks on.
   - A backend with no create or update tool: hand me the page text to paste; never fake a write
     through an issue or a comment. A backend of an unknown kind: say which tool serves each
     operation and how a superseded decision is marked, and get my yes before writing.
2. Read the Backend section of the project's copy of this skill, then
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
