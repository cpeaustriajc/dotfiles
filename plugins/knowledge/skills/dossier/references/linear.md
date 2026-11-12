# Linear adapter

Use the Linear MCP server; look in its tool list for document CRUD and search. If only
`authenticate` tools are listed, ask the user to connect Linear. If there is no create or update
tool, hand the user the page text to paste. Never fake a write through an issue or a comment.

## Layout: no numbers, no index

Search replaces the index and the number; a hand-kept index goes stale here.

- **`Decision: <Topic>`**: one document per decision, topic a plain statement ("Decision: Make
  Offer hidden"). Keep the prefix: a title search lists every decision.
- **First body line:** `**Status:** Accepted · **Kind:** Product · **Decided by:** <name or role>
  · **Date:** YYYY-MM-DD`. `Kind` is Architecture, Product, Process or Business. Then Context,
  Decision and Consequences.
- No `Decisions` index document (if the team keeps one, follow the team and add the row).
- **`Home`**: one paragraph, then the `Page | What it answers` table of research pages only.
- A team `Decision` template in Linear, or a title format in the project's facts, wins.
- **Where:** a decision about one feature goes in that feature's project; one every project
  relies on goes in the team's documents, or on an initiative if it spans only that initiative.

## Issues are first-class

- `Issue` field: the identifier (`ENG-123`), which Linear renders as a live link.
- A decision that came out of an issue also gets a comment on that issue with the decision's
  title.

## Operations

- **Find.** Search for the topic, `Decision:` and "Decided by", across the team and candidate
  projects.
- **Supersede.** Create the new document. In the old one change only the first body line's Status to
  `Superseded by <link>` or `Partly superseded by <link>: <the part>`.
- **A stale detail, not a stale decision.** Strike it in place with `~~…~~` and add a document
  comment saying what replaced it and where that is recorded.

The first write to a team's project follows SKILL.md step 5: show the text first.
