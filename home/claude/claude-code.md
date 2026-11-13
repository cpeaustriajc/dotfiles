- Models: Haiku for mechanical work, Sonnet for specced work, Opus for design and judgment, Fable
  only to coordinate a planned orchestration.
- Effort: medium by default, high for code review, one step up when it keeps failing, `xhigh`
  rarely. `~/.claude/hooks/deny-max-effort.sh` denies `max`.
- Trust the model: a brief gives the goal, the reason and the limits; the worker chooses the
  mechanism and the wording. Before a brief or a prompt, read `~/.claude/prompting.md` for that
  model. Failure: a brief dictated a design from an unchecked reading of an API, and the worker
  redid it.
- `~/.claude/hooks/deny-go-ahead-questions.sh` denies a question that only asks to commit, push or
  open a PR; a project that wants sign-off adds `.claude/wants-sign-off`. Failure: agents asked
  the owner to approve work the owner had already asked for.
