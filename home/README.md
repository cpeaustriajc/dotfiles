# home

This folder holds the author's home folder config for Claude Code, Codex, zsh and the apps that
have text config files: nvim, tmux, Ghostty, Starship, Zed, git, gh and mise.
[home-manager](https://nix-community.github.io/home-manager/) puts the files in `~`.
[`home.nix`](home.nix) lists each file, and [`flake.nix`](../flake.nix) pins the versions of
nixpkgs and home-manager.

The Claude Code folder is `claude/`, not `.claude/`. Claude Code would load a `.claude/` folder
as project config for this repo.

## Set up a new machine

1. Install Nix with the [official installer](https://nixos.org/download/) in multi-user mode.
2. Clone the repo to `~/Projects/dotfiles`. The links in `home.nix` point to this path.
3. Run the first switch. On Linux, use `#cj-linux` in place of `#cj`.

```bash
git clone https://github.com/cpeaustriajc/dotfiles ~/Projects/dotfiles
```

```bash
NIX_CONFIG='extra-experimental-features = nix-command flakes' nix run home-manager/release-26.05 -- switch --flake ~/Projects/dotfiles#cj -b hm-backup
```

Then set the `EMAIL` environment variable to your git email, in the system environment or in a
shell file that is not in this repo. The linked `~/.gitconfig` has no email, because the repo is
public. Without `EMAIL`, git makes an address from your user and host names and prints a warning. Put other machine-only git settings, for example `[safe] directory`,
in `~/.config/git/local`. The linked config includes this file if it exists.

`NIX_CONFIG` turns on flakes for this one run. The `-b hm-backup` flag moves each existing file
in the way to `<name>.hm-backup`, so you lose no live file. The first switch also writes
`~/.config/nix/nix.conf` with flakes on and installs the `home-manager` command.

## Change a file

The way to change a file depends on how home-manager puts it in `~`.

- To change a linked file, edit it here or at its live path. Both paths open the same file, so you
  need no switch.
- To change `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`, edit `agents.md` or
  `claude/claude-code.md`, then run the switch.
- To add a file or a hook, add a line to `home.nix`, then run the switch.

```bash
home-manager switch --flake ~/Projects/dotfiles#cj
```

The linked files are `~/.zshrc`, `~/.gitconfig`, the config of each app in `config/`, and these
files in `~/.claude/`: `statusline-command.sh`, the hooks, `agents/` and `output-styles/`.
Zed, gh, git and mise write their config through the link, so a change from the app lands here.
On macOS, Ghostty also loads `~/Library/Application Support/com.mitchellh.ghostty/config` after
the linked file, and its values win. Keep that file absent, and put each setting in
`config/ghostty/config`.
`CLAUDE.md` is `agents.md` followed by `claude/claude-code.md`. `AGENTS.md` is `agents.md` alone.

To look up an option in `home.nix`, search the
[home-manager options](https://home-manager-options.extranix.com/).

## Sync settings.json

Claude Code rewrites `~/.claude/settings.json` itself, so the file is not a link. Only the keys in
`claude/settings.shared.json` sync. The other live keys stay on the machine.

- At each switch, each shared key replaces its live value. Under `permissions`, only the shared
  sub-keys replace their live values, so the live `allow` and `deny` lists stay.
- To keep a change that Claude Code made to a shared key, run `claude/settings-capture.sh`. The
  script copies the live values of the shared keys into `settings.shared.json`.
- At session start, the `settings-drift.sh` hook prints one line if a shared key differs from
  `settings.shared.json`.

## tmux

This tmux config is deprecated, and nobody maintains it. For parallel sessions, use
`claude agents`. The status bar uses Catppuccin Mocha in dark mode and Latte in light mode.
tmux reads the system appearance when it loads the config. To apply a new appearance, press
`prefix r`.

## Not in this folder

- The `settings.json` keys that `settings.shared.json` does not list, for example hooks, plugins,
  `autoMode` and the `allow` and `deny` lists. To teach auto mode about a machine, run
  `/auto-mode-setup`.
- Machine-only files next to the links: `~/.config/nvim/nvim-pack-lock.json` and each hook in
  `~/.claude/hooks/` that `home.nix` does not list.
- The playwright-cli skill. To install it, run `playwright-cli install --skills -g`.
- Programs: `home.nix` installs each app above except Zed, plus `jq` for the hooks, colima, the Docker CLI
  and lazygit. Homebrew can stay installed next to them; the first `PATH` entry wins.
- Secrets and machine files: the `EMAIL` value, `~/.config/git/local`, `~/.config/gh/hosts.yml`, `~/.ssh/config`,
  `~/.docker/config.json`, `~/.config/op/`.
- Zed itself, opencode and its config, and VS Code.
- `~/.colima/default/colima.yaml`. Colima writes this file again at each `colima start`
  (`--save-config` is on by default), so it is not a link.
- Zed's `settings_backup.json` and lazygit's empty `config.yml`.
- Machine state: transcripts, history, caches and backups.
