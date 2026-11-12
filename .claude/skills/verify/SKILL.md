---
name: verify
description: >
  This skill should be used before a commit or a push in dotfiles, and when the user says "verify
  this" or "prove it works". It maps the diff to features, runs each feature's checks with their
  real exit codes, saves the logs and prints one result line per feature: VERIFIED, NOT VERIFIED
  or BLOCKED.
user-invocable: false
---

# Verify

1. **Launch**: no app. The run skill `run-dotfiles` owns the driver, `smoke.sh`.
2. **Doctor**: `command -v claude python3 bash git`, then `python3 -c 'import yaml'` or
   `command -v uv`. A missing one is BLOCKED: name it.
3. **Select** and **Drive** (default base `origin/main`):
   `.claude/skills/verify/select.sh [base] | .claude/skills/verify/drive.sh <scratchpad>/verify`,
   with the session's scratchpad directory. Without the argument, logs go under `$TMPDIR`.
   Features live in `references/features/`. Markdown is the product, so a docs-only diff runs too.
4. Zero tests run is NOT VERIFIED (mods: `references/features/mods.md`). Then do each feature's
   **Check** line by hand and note it in its log.
5. **Evidence**: print the log folder, `<scratchpad>/verify/<short sha>/`. The OS empties it, so
   the result lines, with their re-run commands, are the record that lasts.
6. **Cleanup**: none. `smoke.sh` removes its own config directory.
7. **Full suite**: `.claude/skills/run-dotfiles/smoke.sh all` before every push to `main`. Exit 2
   is BLOCKED, not a pass.
8. **Result line**: one per feature, then the overall result, VERIFIED only when every feature is.

```
<feature>: VERIFIED | NOT VERIFIED | BLOCKED  cmd: <re-run command>  evidence: <path>
```
