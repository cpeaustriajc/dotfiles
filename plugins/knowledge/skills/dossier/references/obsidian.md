# Obsidian adapter

A vault is a folder of Markdown: the file tools are the adapter. The pointer names a folder
inside the vault (`obsidian: ~/Vaults/Work/Projects/acme`).

## Layout

`Home.md`, `Decisions.md` and one `Decision NNN <Topic>.md` per decision, plus research pages, all
in that folder. Put the metadata in frontmatter as well as the Status line, so Dataview or Bases
can build the newest-first index:

```yaml
---
type: decision
number: 7
status: accepted        # proposed | accepted | partly-superseded | superseded
date: 2026-09-18
superseded_by: "[[Decision 009 …]]"
issue: https://github.com/o/r/issues/27
---
```

Keep the hand-written index table in `Decisions.md` anyway: it renders on GitHub and in plain
editors, where no Dataview runs.

## Saving

- A git vault (Obsidian Git): commit after each change; no push unless the user syncs that way.
- A synced vault: saving is publishing, so show the user first. Synced means its path is under
  `~/Library/Mobile Documents/` or a Dropbox, Google Drive or OneDrive folder; or
  `.obsidian/core-plugins.json` enables `sync`; or `.obsidian/plugins/` holds a sync or git
  plugin. Unsure: ask. Don't assume the vault is private.
