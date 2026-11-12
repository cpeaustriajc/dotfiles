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

The product is the marketplace as Claude Code installs it. From the repo root, with `claude`,
`python3`, `bash`, and PyYAML or `uv`:

```bash
.claude/skills/run-dotfiles/smoke.sh all       # about 5 min; exit 0 pass, 1 fail, 2 blocked
.claude/skills/run-dotfiles/smoke.sh validate  # claude plugin validate .
.claude/skills/run-dotfiles/smoke.sh tests     # mod tests, scripts/check_*.py, tests_kept.py, every test file
.claude/skills/run-dotfiles/smoke.sh selftest  # about 4 min; canaries: each runner goes red on a failing test
.claude/skills/run-dotfiles/smoke.sh details   # skills and token cost, always-on and on-invoke
.claude/skills/run-dotfiles/smoke.sh doctor    # /skill-doctor with the skill plugins installed
claude plugin test mods/<mod>                  # one mod
python3 -I plugins/planning/skills/shape/scripts/test_check_tree.py  # one script
bash plugins/knowledge/skills/hone/scripts/test_corrections.sh
python3 -I plugins/engineering/skills/review-loop/scripts/tests_kept.py [--base <ref>]  # tests weakened?
```

`details` and `doctor` install the working tree into a temporary config, so `~/.claude` stays
unchanged. Before you read a failure, a BLOCKED or an empty column as a result, read
`references/gotchas.md`.
