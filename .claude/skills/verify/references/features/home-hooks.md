# Home hooks

What exists: each `home/claude/hooks/<hook>.sh` is a Claude Code hook that home-manager links
into `~/.claude/hooks/`. A hook with tests has `home/claude/hooks/tests/<hook>.test.sh`.

- **Code:** `home/claude/hooks/**`
- **Tests:** each `home/claude/hooks/tests/*.test.sh`; each ends with `N passed, 0 failed`.
- **Check:** `ls -l ~/.claude/hooks/<hook>.sh` points into this checkout, and
  `jq '.hooks.PreToolUse' ~/.claude/settings.json` lists the hook with its matcher.
