#!/usr/bin/env bash
# SessionStart: one line when synced settings.json keys drift from the source, silent otherwise.
# Source: ~/Projects/dotfiles/home/claude/settings.shared.json. Only its keys are synced; other
# live keys belong to the machine. The other ~/.claude files are links into the checkout, so
# they cannot drift.
set -euo pipefail

public=~/Projects/dotfiles/home/claude/settings.shared.json
live=~/.claude/settings.json
[ -s "$live" ] || live=/dev/null

keys="$(jq -rn --slurpfile l "$live" --slurpfile s "$public" '
  ($l[0] // {}) as $l | $s[0] as $s
  # Under "permissions" only the listed sub-keys are synced, as in the home.nix merge.
  | [ $s | keys[] | . as $k
      | ($l[$k] // null) as $v
      | select(if $k == "permissions"
          then ($v // {} | with_entries(select(.key as $x | $s.permissions | has($x))))
          else $v end != $s[$k]) ]
  | join(", ")')"

[ -z "$keys" ] || echo "settings.json: $keys differ from the sources; capture a live edit with settings-capture.sh"

