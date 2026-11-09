---
name: run-dotfiles
description: >
  This skill should be used to run, test, validate or inspect the dotfiles marketplace as Claude
  Code loads it: plugin validation, every mod's tests, the skill script tests, plugin token costs,
  /skill-doctor with the skill plugins installed. Use it before
  committing a change to a skill, mod or manifest, or to see what a skill costs per turn.
user-invocable: false
---

# Run dotfiles

dotfiles has no app to launch: the "running" product is the marketplace as Claude Code installs
it. The driver is `.claude/skills/run-dotfiles/smoke.sh`, which validates it, runs every test
suite, installs the skill plugins into a throwaway config directory and asks Claude Code what it loaded.
Paths here are relative to the repo root.

## Prerequisites

`claude`, `python3` and `bash`, plus PyYAML or `uv` (the descriptions check uses `uv run --with pyyaml` when `python3` lacks it). Nothing to build.

## Run (agent path)

```bash
.claude/skills/run-dotfiles/smoke.sh all       # everything, about 20 s; exit 0 pass, 1 fail, 2 blocked
.claude/skills/run-dotfiles/smoke.sh validate  # claude plugin validate .
.claude/skills/run-dotfiles/smoke.sh tests     # each mod's hook tests + skill script tests
.claude/skills/run-dotfiles/smoke.sh details   # skills and per-skill token cost, always-on and on-invoke
.claude/skills/run-dotfiles/smoke.sh doctor    # /skill-doctor with the skill plugins installed
```

`doctor` and `details` install the local working tree (not the pushed one) into a `mktemp -d`
config directory, so your real `~/.claude` never changes and the temp directory is removed on
exit.

One mod or script at a time:

```bash
claude plugin test mods/linear-gate
python3 -I plugins/planning/skills/shape/scripts/test_check_tree.py
bash plugins/knowledge/skills/hone/scripts/test_corrections.sh
```

## Gotchas

- **`/skill-doctor` runs headless**: `claude -p "/skill-doctor"` prints its table and exits.
- **`--plugin-dir .` loads none of dotfiles's skills.** The repo root is a marketplace
  (`.claude-plugin/marketplace.json`, one source per plugin such as `./plugins/planning`), not a plugin,
  so skill-doctor shows only claude.ai and user skills. Install from the local marketplace instead,
  as the driver does.
- **A fresh `CLAUDE_CONFIG_DIR` is signed out on macOS** (the sign-in is in the keychain under the
  default config). `doctor` signs in with `CLAUDE_CODE_OAUTH_TOKEN`, read from 1Password
  (`op://Personal/Claude Code OAuth token/credential`) when it is not set; without either it prints
  `BLOCKED` and smoke exits 2.
- **The 7-day token and use columns are always empty** in the driver's throwaway config: they come
  from this machine's past sessions. For real usage, run `claude -p "/skill-doctor"` with your own
  config after installing the plugin there.
- **`claude plugin validate plugins/<plugin>/skills/<skill>` always fails** with "No manifest found": a
  skill folder is not a plugin. Validate the repo root.
- **Python scripts leave `__pycache__`** in the skill folder; the driver deletes it, and
  `.gitignore` covers it.

## Not in the driver

- **Descriptions** follow plugin-dev's rules (`tests` checks them): third person ("This skill
  should be used when…"), at most 500 characters, and a `>` block scalar, since an unquoted
  description containing `": "` is invalid YAML that `claude plugin validate` doesn't catch.
