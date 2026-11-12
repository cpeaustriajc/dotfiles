---
paths:
  - "plugins/**"
  - "mods/**"
  - "**/.claude-plugin/*.json"
  - "AGENTS.md"
---

# Claude Code commands for the authoring steps

`AGENTS.md` says to run `run-dotfiles` after a change. This file gives the Claude Code command
for it. Use what Claude Code ships before writing your own checks.

## Validate the manifests

- `claude plugin validate .` after any manifest, skill or frontmatter change.

## Check a plugin's components and token cost

- `claude plugin details <plugin>` for a plugin's components and projected token cost.

## Run a mod's hook tests

- `claude plugin test mods/<mod>` for a mod's hook tests.

## Audit the instruction files

- `/doctor prompt-audit` when a new frontier model ships, and `/doctor prompt-audit <path>` after
  editing a skill or rule: flags dated instructions, conflicts and missing files. Headless runs
  skip `~/.claude` unless given `--add-dir ~/.claude`.
- `claude-md-improver` (claude-md-management) when CLAUDE.md drifts from the code;
  `/revise-claude-md` at the end of a session that exposed missing context.

## Draft skills and plugin parts

- `skill-creator` and `plugin-dev` (claude-plugins-official) for drafting skills and plugin parts.
