#!/usr/bin/env bash
# Maps the diff against a base (default origin/main) to features, one line each: feature<TAB>command.
set -uo pipefail
base="${1:-origin/main}"
cd "$(git rev-parse --show-toplevel)"
files="$(git diff --name-only "$base"...HEAD; git diff --name-only; git diff --name-only --cached; git ls-files --others --exclude-standard)"
files="$(printf '%s\n' "$files" | sort -u | sed '/^$/d')"
[[ -z "$files" ]] && { echo "no changes against $base"; exit 0; }
printf '%s\n' "$files" | grep -q -E '^plugins/|^\.claude/skills/|^scripts/' && printf 'skills\t.claude/skills/run-dotfiles/smoke.sh tests\n'
for mod in $(printf '%s\n' "$files" | sed -n -E 's#^mods/([^/]+)/.*#\1#p' | sort -u); do
  [[ -d "mods/$mod/hooks" ]] && printf 'mod %s\tclaude plugin test mods/%s\n' "$mod" "$mod"
done
printf '%s\n' "$files" | grep -q -E '^mods/|^tests/claude-owned/' && printf 'claude-owned\tpython3 tests/claude-owned/run.py\n'
printf '%s\n' "$files" | grep -q -E '^home/claude/hooks/' && printf 'home hooks\tfor t in home/claude/hooks/tests/*.test.sh; do bash "$t" || exit 1; done\n'
printf '%s\n' "$files" | grep -q -E '\.claude-plugin/|README\.md$|^scripts/(test_)?check_readmes\.py$' && printf 'manifests\tclaude plugin validate .\n'
# Graders: the files that judge a change (scripts/graders_changed.py). Prove they still go red.
printf '%s\n' "$files" | grep -q -E '^\.github/|^scripts/|^\.claude/skills/(verify|run-dotfiles)/|^plugins/engineering/skills/review-loop/scripts/|^tests/claude-owned/' \
  && printf 'graders\t.claude/skills/run-dotfiles/smoke.sh selftest\n'
printf '%s\n' "$files" | grep -q -E '^\.github/' && printf 'ci\tcommand -v actionlint >/dev/null || { echo "BLOCKED: actionlint is not installed (brew install actionlint)"; exit 2; }; actionlint .github/workflows/*.yml && echo "actionlint ok" && python3 -m json.tool .github/rulesets/main.json >/dev/null && echo "ruleset ok"\n'
exit 0
