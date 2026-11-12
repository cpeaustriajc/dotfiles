# Claude Code adapter

- The work folder is the session's scratchpad directory. A later session cannot find it, so it
  never reads an old ledger as current.
- Hunters are `Agent` calls with `model` one step cheaper than the session's and
  `effort: "high"`, unless I name another model: a fix needs design calls, so not the cheapest
  model. Send all three `Agent` calls in one message.
- "One model tier up" stops at the session's own model. A subagent never runs on a model above
  the session's.
- Do not use `/code-review` as the hunter. Its `--fix` applies the findings after the review,
  with no failing test first, to any file, not only the hunter's shard. A second `/code-review`
  started while one runs goes to the foreground, so three cannot run in parallel. Source:
  https://code.claude.com/docs/en/code-review-local, sections "Tune effort and arguments" and
  "Run in the foreground".
- All hunters work in the session's own worktree. Disjoint shards keep their edits apart; never
  give them `isolation: "worktree"`, because their fixes must see each other next round.
- A `Workflow` script can run the rounds only when I ask for a workflow.
