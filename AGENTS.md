# dotfiles: rules for every coding agent

`CLAUDE.md` imports this file, so Claude Code and Codex read the same rules.

## Trunk-based development

- Commit each finished slice to `main`, and push it after `/verify` passes.
- Open no pull request and no PR stack in this repo. This overrides the global rules that open
  them.
- A worktree branch lives less than a day: rebase it on `main`, fast-forward `main` to it, push
  `main`, then delete the branch.
- Failure: a side branch drifts from `main`, and its merge or restack redoes work.
- `python3 -I scripts/check_trunk.py` fails on a branch older than a day with commits not on
  `main`.

## Writing

- In prose that a person reads (a commit message, README, issue or reply), state each finding
  and cite what you checked. Skip "it's not X, it's Y", verdict headings, moral closers, and an
  adverb or "nothing" or "never" with no check behind it.
- Failure: declauding's corpus (oaustegard/claude-skills) counts PR descriptions written
  this way at 0.70% in early 2025 and 39.5% in August 2026.

## Writing instructions for a model

- Say what to do and give its reason; a model generalizes from the reason. Keep "never" for a
  hard limit, and leave "MUST", "CRITICAL" and all-caps words out.
- Failure: Anthropic's prompting best practices say newer Claude models over-apply rules
  written in aggressive language, and mark a bare "NEVER use ellipses" as less effective
  than the same rule with its reason.
- No word makes a model obey every time. A rule that must always hold needs a check.
