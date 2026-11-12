# Notion adapter

Use the Notion MCP server (search and page CRUD; find the names in the tool list). If only
`authenticate` tools are listed, ask the user to connect Notion first.

## Layout

- **A root page** is Home: one paragraph, then a table or list of child pages with what each
  answers.
- **The decision log is a database** under the root, named `Decisions`:
  - `Name` (title): the full "Decision NNN: <Topic>"
  - `Number`
  - `Status`: select of Proposed, Accepted, Partly superseded, Superseded
  - `Superseded part`: text naming what a partial supersede replaced
  - `Date`
  - `Issue`: URL
  - `Superseded by`: relation to the same database

  The default view sorts by `Date` descending. A row's body holds Context, Decision and
  Consequences as headings.
- **Research pages** are child pages of the root.
- A team's existing decisions database with other property names: map onto it, do not create a
  second.

## Operations

- **Find.** A pointer URL's trailing 32-character hex string is the page or database id.
- **Record.** Highest `Number` plus one.
- **Supersede.** On the old row set `Status` (Superseded, or Partly superseded with
  `Superseded part`) and fill `Superseded by`. Leave its body untouched.
- **Link** with a page mention, not a pasted URL, so a rename does not break it.

Notion saves as you write and the whole workspace sees it at once, hence SKILL.md step 5's review
before the first write.
