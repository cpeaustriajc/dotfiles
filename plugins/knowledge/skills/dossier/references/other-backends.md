# Other backends

SKILL.md and `shape.md` conventions hold. Map find, read, record and supersede onto the backend's
MCP server or CLI.

- **Confluence** (Atlassian MCP, or `twg confluence` where installed): a space or parent page is
  Home; a `Decisions` child page holds the index table; each decision is its child page titled
  `Decision NNN: <Topic>`. Page history is no licence to rewrite a superseded page: Status only.
  Keep the hand-written table even if Page Properties hold Status and Date.
- **Google Docs / Drive** (Drive MCP): a folder is Home; `Decisions` is one Doc holding the index
  table; each decision is a Doc in a `Decisions` subfolder. Link with the Doc URL.
- **Anything else:** before writing, tell the user which tool serves each operation and how a
  superseded decision will be marked, and get a yes. Record the mapping in the `"notes"` field of
  that entry in `${XDG_CONFIG_HOME:-~/.config}/dossier/dossier.json`.
