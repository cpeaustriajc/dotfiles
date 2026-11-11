# Shape of the knowledge

Step 2 of SKILL.md reads this. Where a backend's adapter gives its own shape, the adapter wins.

## Pages

- **Home** (or the workspace's root page). One paragraph says the README is the product spec,
  meaning what we build, and the decisions record why. Below it, a `Page | What it answers` table
  lists every page.
- **Decisions index.** A table, newest first by date, with columns `# | Decision | Status | Date |
  Issue`. A new row goes at the top. Sort by date, not by number: numbers follow the order
  decisions were recorded, and they can be out of date order.
- **`Decision NNN <Topic>`.** One page per decision, numbered with zero padding (`001`). Its facts
  and wording stay as they were decided, so a reader can trust any old decision page as a record
  of what was known then.
- **Backends with search but no sorted views** (Linear) drop the number and the index: each
  decision is titled `Decision: <Topic>` and found by search. Their adapter gives the shape that
  replaces the two items above.
- **Research pages.** One topic each. Date the research, and mark anything not confirmed on a
  primary source as **UNVERIFIED**. When newer facts replace what a page describes, rewrite the
  page to describe the current state, and move the old description under `## History` at the
  foot, saying what replaced it. Deleting it would erase the evidence behind older decisions.

## Decision template

```markdown
# Decision NNN: <Topic>

**Status:** Proposed | Accepted | Superseded by [[Decision NNN …]] | Partly superseded by [[Decision NNN …]]: <the part>
**Date:** YYYY-MM-DD · **Issue:** [#N](link) or "none recorded"

## Context
The problem, and links to the research pages.

## Decision
What we chose.

## Consequences
What it rules out and what it costs.
```

Use the backend's own link syntax: `[[Page]]` on a wiki or in Obsidian, a page mention in Notion.

## Dates

A decision's date comes from something a reader can check: the commit or session that acted on
it (or the log of the files it changed), an issue, or my word. If none exists, write the month
and say that the day is not recorded. A decision and its build are different events, so a page
may carry both: `**Built:** YYYY-MM-DD (<sha>)`.
