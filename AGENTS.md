# dotfiles

A skill names no harness and holds no project's facts.

- GitHub flow. `/verify` before push.
- Don't fight the harness. No Not-Invented-Here. YAGNI. Single source of truth.
- No AI slop. Known terms over explanations. Audit on each frontier model release.
- Prior art: evidence over authority (`SOURCES.md`).
- Before adding: `SCOPE.md`, `models/README.md`. After a change: `run-dotfiles`.
- Marketplace: `.claude-plugin/marketplace.json` is the manifest; a mod's `plugin.json` holds
  `name`, `types`, `userConfig` and copies `displayName`, `description`, `author` (the app shows
  those; `scripts/check_mod_manifests.py`).
- Vendor-neutral skills; code-host and tracker adapters: `references/<host>.md`; typed skills need
  `agents/openai.yaml`.
- Home-manager flake, public repo: `home/claude/` is `~/.claude`; `settings.json` syncs only
  `settings.shared.json` keys.
- Checks: `scripts/check_*.py`, `tests/claude-owned/run.py`.
