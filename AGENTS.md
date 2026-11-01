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
