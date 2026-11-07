# home

The author's home folder: Claude Code and Codex config, zsh, nvim and tmux. A standalone
[home-manager](https://nix-community.github.io/home-manager/) config puts these files in `~`.
`flake.nix` at the repo root pins nixpkgs and home-manager; `home.nix` in this folder lists the files.
The Claude Code folder is `claude/`, not `.claude/`, so that Claude Code does not load it as
project config in this repo.

## Install on a new machine

1. Install Nix with the [official installer](https://nixos.org/download/) (multi-user).
2. Clone the repo to `~/Projects/dotfiles`. The links point there, so use this path.
3. Run the switch below. `-b hm-backup` renames each live file in the way to `<name>.hm-backup`.

```bash
git clone https://github.com/cpeaustriajc/dotfiles ~/Projects/dotfiles
```

```bash
NIX_CONFIG='extra-experimental-features = nix-command flakes' nix run home-manager/release-26.05 -- switch --flake ~/Projects/dotfiles#cj -b hm-backup
```

`NIX_CONFIG` turns on flakes for this run and for the `nix` calls that home-manager makes.
On Linux, use `#cj-linux` in place of `#cj`. The first switch writes `~/.config/nix/nix.conf`
with flakes on and installs the `home-manager` command, so later runs need no extra flags.

## What is in this folder

| Live file | Source |
|-----------|--------|
| `~/.zshrc` | link to `zshrc` |
| `~/.claude/statusline-command.sh`, `hooks/*`, `agents/`, `output-styles/`, `skills/workflow-models/` | links into `claude/` |
| `~/.claude/CLAUDE.md` | generated: `agents.md`, then `claude/claude-code.md` |
| `~/.codex/AGENTS.md` | generated: `agents.md` alone |
| `~/.claude/settings.json` | only the keys in `claude/settings.shared.json`, merged at each switch; every other live key keeps its value |
| `~/.config/nvim/init.lua`, `lua/` | links into `config/nvim/` |
| `~/.config/tmux/` | link to `config/tmux/`; `tmux.conf` picks the macOS or Linux lines at run time |

tmux is deprecated: it is no longer maintained. Use `claude agents` for parallel sessions. The
status bar uses Catppuccin Mocha (dark) or Latte (light), chosen from the system appearance when
the config loads. After you change the appearance, press `prefix r` to reload.

## Change a file

- A linked file: edit it here or live. Both are the same file, so no switch is needed.
- A generated file, a new link or a new hook: edit `home.nix` or its source, then run the switch.

```bash
home-manager switch --flake ~/Projects/dotfiles#cj
```

- `settings.json` syncs only the keys in `claude/settings.shared.json`. To keep an app change to
  one of those keys, run `claude/settings-capture.sh`: it copies their live values here.
- The `settings-drift.sh` hook reports at session start when a synced key differs from this folder.
- To look up an option, search the [home-manager options](https://home-manager-options.extranix.com/).

## Not in this folder

- Every other `settings.json` key: hooks, plugins, permissions, `autoMode` and the UI choices.
  Each machine sets them itself; run `/auto-mode-setup` to teach auto mode about the machine.
- Machine-only files beside the links: `~/.config/nvim/nvim-pack-lock.json` and any other hook in `~/.claude/hooks/`.
- The playwright-cli skill: `playwright-cli install --skills -g` installs it.
- Programs: nvim, tmux and the rest come from Homebrew or mise. Nix installs only `jq`.
- Machine state: transcripts, history, caches, backups.
