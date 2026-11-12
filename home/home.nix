{ config, pkgs, lib, ... }:

let
  # A link into the checkout, not into the Nix store: a live edit lands in the repo.
  # The repo must be cloned at ~/Projects/dotfiles.
  link = path: config.lib.file.mkOutOfStoreSymlink "${config.home.homeDirectory}/Projects/dotfiles/home/${path}";
in
{
  home.username = "cj";
  home.homeDirectory = if pkgs.stdenv.isDarwin then "/Users/cj" else "/home/cj";
  home.stateVersion = "26.05";

  programs.home-manager.enable = true;

  # The Claude Code hooks need jq.
  home.packages = [
    pkgs.jq
    (if pkgs.stdenv.isDarwin then pkgs.ghostty-bin else pkgs.ghostty)
    pkgs.starship
    pkgs.git
    pkgs.gh
    pkgs.mise
    pkgs.colima
    pkgs.docker-client
    pkgs.neovim
    pkgs.tmux
    pkgs.lazygit
  ];

  # Writes ~/.config/nix/nix.conf, so later runs need no --extra-experimental-features.
  nix.package = pkgs.nix;
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  home.file = {
    ".zshrc".source = link "zshrc";

    ".claude/CLAUDE.md".text = builtins.readFile ./agents.md + "\n" + builtins.readFile ./claude/claude-code.md;
    ".codex/AGENTS.md".text = builtins.readFile ./agents.md + "\n";

    ".claude/statusline-command.sh".source = link "claude/statusline-command.sh";
    ".claude/agents".source = link "claude/agents";
    ".claude/output-styles".source = link "claude/output-styles";
    # One link per hook: the live hooks folder also holds machine-only hooks.
    ".claude/hooks/deny-1m-subagent.sh".source = link "claude/hooks/deny-1m-subagent.sh";
    ".claude/hooks/deny-max-effort.sh".source = link "claude/hooks/deny-max-effort.sh";
    ".claude/hooks/deny-linear-engineering-text.sh".source = link "claude/hooks/deny-linear-engineering-text.sh";
    ".claude/hooks/deny-migrations.sh".source = link "claude/hooks/deny-migrations.sh";
    ".claude/hooks/deny-go-ahead-questions.sh".source = link "claude/hooks/deny-go-ahead-questions.sh";
    ".claude/hooks/thread-needs-model-and-effort.sh".source = link "claude/hooks/thread-needs-model-and-effort.sh";
    ".claude/hooks/settings-drift.sh".source = link "claude/hooks/settings-drift.sh";

    # nvim writes nvim-pack-lock.json into its config folder; it stays on the machine.
    ".config/nvim/init.lua".source = link "config/nvim/init.lua";
    ".config/nvim/lua".source = link "config/nvim/lua";
    ".config/tmux".source = link "config/tmux";

    ".config/ghostty/config".source = link "config/ghostty/config";
    ".config/starship.toml".source = link "config/starship.toml";
    # Zed itself is installed outside Nix. Zed writes settings.json from its UI. It writes to the link target, so the link stays.
    ".config/zed/settings.json".source = link "config/zed/settings.json";
    ".config/zed/keymap.json".source = link "config/zed/keymap.json";
    # [user] and machine paths go in ~/.config/git/local, which is not in the repo.
    ".gitconfig".source = link "config/git/gitconfig";
    ".config/git/ignore".source = link "config/git/ignore";
    # hosts.yml holds the gh token and stays on the machine.
    ".config/gh/config.yml".source = link "config/gh/config.yml";
    ".config/mise/config.toml".source = link "config/mise/config.toml";
  };

  # Claude Code rewrites ~/.claude/settings.json itself, so it is not a link. Only the keys of
  # claude/settings.shared.json are synced: they replace the live values. Under "permissions"
  # only the listed sub-keys replace, so the live allow and deny lists stay. Every other live key
  # keeps its value and its place. A new key goes at the end.
  home.activation.claudeSettings = lib.hm.dag.entryAfter [ "writeBoundary" ] ''
    live="$HOME/.claude/settings.json"
    src=/dev/null
    [ -f "$live" ] && src="$live"
    tmp="$(mktemp)"
    ${pkgs.jq}/bin/jq -n --slurpfile shared ${./claude/settings.shared.json} '
      $shared[0] as $s
      | reduce ($s | keys[]) as $k (first(inputs) // {};
          .[$k] = if $k == "permissions" then (.permissions // {}) * $s.permissions else $s[$k] end)
    ' "$src" > "$tmp"
    if ! cmp -s "$tmp" "$live"; then
      run mkdir -p "$HOME/.claude"
      run install -m 600 "$tmp" "$live.hm-tmp"
      run mv "$live.hm-tmp" "$live"
    fi
    rm -f "$tmp"
  '';
}
