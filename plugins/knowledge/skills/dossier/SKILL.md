---
name: dossier
description: >
  This skill should be used when the user says "note that down as a decision", "what did we decide
  about X", "supersede that decision" or "record this research". It keeps the project's dossier:
  decision and research pages in the team's wiki or Notion. Agent rules: the instruction file.
---

Decision log and research pages live where the team writes, not in the code repo (an existing
`docs/adr/` is followed: `references/shape.md`), and are written for people; agent instructions
go in the project's instruction file. Paths are relative to this skill's folder.

1. Find the log in the order of `references/locate.md`. When the project's skills folder has no
   copy of this skill, set up first, then run the copy from its step 2:
   - Find what reaches the backend: the connected tools' lists, the CLI's `--help`, a folder of
     files. Read its page and link rules, and the log's newest pages.
   - Write the copy in that folder: this file without these Setup bullets, every file the copy
     uses directly or through another file (copied into its folder, paths rewritten), and a
     description with only the triggers it serves. Add a Backend section: which tool serves find,
     read, record, supersede and link; where Home, the decision log and the research pages sit;
     the page-name and link rules; how a save happens. Put `# <plugin> <version>` (from the
     marketplace manifest or this skill's version folder) on the line after the opening `---`.
     Commit it alone under the project's branch rules, else on a new branch, with hooks on.
   - A backend with no create or update tool: hand me the page text to paste; never fake a write
     through an issue or a comment. A backend of an unknown kind: say which tool serves each
     operation and how a superseded decision is marked, and get my yes before writing.
2. Read the copy's Backend section, then `references/shape.md`. Before the first write, learn the
   log's own conventions; they win over the Backend section, and it over `shape.md`.
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
