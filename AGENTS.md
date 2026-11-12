# dotfiles

- GitHub flow. `/verify` before push.
- Don't fight the harness. No Not-Invented-Here. YAGNI. Single source of truth.
- No AI slop. Known terms over explanations. Audit on each frontier model release.
- Prior art: evidence over authority (`SOURCES.md`).
- Before adding: `SCOPE.md`, `models/README.md`. After a change: `run-dotfiles`.
- Marketplace: `.claude-plugin/marketplace.json` is the only manifest; a mod's `plugin.json`
  holds only `name`, `types`, `userConfig`.
- Vendor-neutral skills, ports and adapters: `references/<tool>.md`; typed skills need
  `agents/openai.yaml`.
- Home-manager flake, public repo: `home/claude/` is `~/.claude`; `settings.json` syncs only
  `settings.shared.json` keys.
- Checks: `scripts/check_*.py`, `tests/claude-owned/run.py`.
