# Claude Code adapter

- Draft space: a Claude Docs doc when its connector is attached, else a private Artifact, else
  the session's scratchpad as `draft-<n>.md`, `review-<n>.md` and `decisions-<n>.md`.
- Spikes: `Agent` with `subagent_type: "Explore"` (Haiku) for code and file lookups,
  `general-purpose` on `model: "sonnet"` for the tracker, the web or a browser run. Start them in
  one message so they run together.
- Cold read: `Agent` on `model: "opus"` while a round still finds blockers, `model: "sonnet"`
  once the last read found only slips. Effort per `~/.claude/CLAUDE.md`.
- Applying decided fixes: `Agent` on `model: "sonnet"`, given the decision log.
- Ask with `AskUserQuestion`, each option with its confidence.
- A long session keeps the round, the open decisions and the spikes run in one place I can open,
  per `~/.claude/CLAUDE.md`.
