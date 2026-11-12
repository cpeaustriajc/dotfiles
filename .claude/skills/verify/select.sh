#!/usr/bin/env bash
# Maps the diff against a base (default origin/main) to features, one line each: feature<TAB>command.
set -uo pipefail
base="${1:-origin/main}"
cd "$(git rev-parse --show-toplevel)"
files="$(git diff --name-only "$base"...HEAD; git diff --name-only; git diff --name-only --cached)"
files="$(printf '%s\n' "$files" | sort -u | sed '/^$/d')"
[[ -z "$files" ]] && { echo "no changes against $base"; exit 0; }
printf '%s\n' "$files" | grep -q -E '^plugins/|^\.claude/skills/' && printf 'skills\t.claude/skills/run-dotfiles/smoke.sh tests\n'
for mod in $(printf '%s\n' "$files" | sed -n -E 's#^mods/([^/]+)/.*#\1#p' | sort -u); do
  [[ -d "mods/$mod/hooks" ]] && printf 'mod %s\tclaude plugin test mods/%s\n' "$mod" "$mod"
done
printf '%s\n' "$files" | grep -q -E '^mods/|^tests/claude-owned/' && printf 'claude-owned\tpython3 tests/claude-owned/run.py\n'
printf '%s\n' "$files" | grep -q -E '^home/claude/hooks/' && printf 'home hooks\tfor t in home/claude/hooks/tests/*.test.sh; do bash "$t" || exit 1; done\n'
printf '%s\n' "$files" | grep -q -E '\.claude-plugin/|README\.md$|^scripts/(test_)?check_readmes\.py$' && printf 'manifests\tclaude plugin validate .\n'
exit 0
