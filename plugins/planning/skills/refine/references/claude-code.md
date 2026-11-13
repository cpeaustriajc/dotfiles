# Claude Code adapter

- Draft space: a Claude Docs doc when its connector is attached, else a private Artifact, else
  the session's scratchpad as `draft-<n>.md`, `review-<n>.md` and `decisions-<n>.md`.
- Spikes: `Agent` with `subagent_type: "Explore"` (Haiku) for code and file lookups,
  `general-purpose` on `model: "sonnet"` for the tracker, the web or a browser run. Start them in
  one message so they run together.
- Cold read: `Agent` on `model: "opus"` for the first full read, `model: "sonnet"` for each
  re-check. Effort per `~/.claude/CLAUDE.md`.
- Drafts and decided fixes: `Agent` on `model: "sonnet"`, given the decision log.
- `/goal`: "the last re-check found 0 blockers, and every open item is in the risk log with a
  mitigation or an accept".
- Ask with `AskUserQuestion`, each option with its confidence.
- A long session keeps the round, the open decisions and the spikes run in one place I can open,
  per `~/.claude/CLAUDE.md`.
