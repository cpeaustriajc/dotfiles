# Features

One file per feature. **Code** lists the paths it owns; `select.sh` maps a diff to features
by these paths. **Tests** and **Check** are the commands that prove it. `drive.sh` runs each
command here and in a clean clone of the base, and `results.py` gives the verdict from the
runners' own result lines.

| Feature | File | Code |
|---|---|---|
| Skills | [skills.md](skills.md) | `plugins/**`, `.claude/skills/**` |
| Mods | [mods.md](mods.md) | `mods/<mod>/**`, `tests/claude-owned/**` |
| Home hooks | [home-hooks.md](home-hooks.md) | `home/claude/hooks/**` |
| Manifests and READMEs | [manifests.md](manifests.md) | `**/.claude-plugin/**`, `README.md`, `**/README.md`, `scripts/check_readmes.py` |
| Graders and CI | [graders.md](graders.md) | `.github/**`, `scripts/**`, `.claude/skills/{verify,run-dotfiles}/**`, `review-loop/scripts/**`, `tests/claude-owned/**` |
