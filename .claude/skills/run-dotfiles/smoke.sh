#!/usr/bin/env bash
# Drives the dotfiles marketplace the way a user's Claude Code sees it.
# Usage (from the repo root): .claude/skills/run-dotfiles/smoke.sh [validate|tests|selftest|doctor|details|all]
set -uo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$root"
step="${1:-all}"; failed=0; blocked=0
say() { printf '\n== %s\n' "$*"; }
run() { "$@" || { failed=1; echo "FAILED: $*"; }; }
# The skill plugins: one folder each under plugins/, with its skills in plugins/<plugin>/skills/.
plugins=(); for d in plugins/*/; do plugins+=("$(basename "$d")"); done

# A throwaway config dir with the local marketplace installed, so the real ~/.claude is untouched.
installed() {
  [[ -n "${cfg:-}" ]] && return
  cfg="$(mktemp -d)"; trap 'rm -rf "$cfg"' EXIT
  CLAUDE_CONFIG_DIR="$cfg" claude plugin marketplace add "$root" >/dev/null
  for p in "${plugins[@]}"; do CLAUDE_CONFIG_DIR="$cfg" claude plugin install "$p@dotfiles" >/dev/null; done
}

validate() { say "validate"; run claude plugin validate .; }

tests() {
  for mod in mods/*/; do
    compgen -G "$mod/hooks/*.test.ts*" >/dev/null || continue
    say "mod tests: $mod"; run bash -c "set -o pipefail; claude plugin test '$mod' 2>&1 | tail -3"
  done
  say "claude-owned: no mod denies or approves what Claude Code decides"
  run python3 tests/claude-owned/run.py
  say "checks: READMEs, typed skills, tracker terms, trunk (scripts/check_*.py)"
  for c in scripts/check_*.py; do run python3 -I "$c"; done
  say "tests kept: no base test line changed or removed, no count dropped, no rig added"
  run python3 -I plugins/engineering/skills/review-loop/scripts/tests_kept.py
  say "skill descriptions: valid YAML, at most 500 characters, third person (plugin-dev's rules)"
  local py=(python3 -)
  python3 -c 'import yaml' 2>/dev/null || py=(uv run --quiet --no-project --with pyyaml python3 -)
  run "${py[@]}" <<'PY'
import glob, sys, yaml
bad = 0
for f in sorted(glob.glob("plugins/*/skills/*/SKILL.md") + glob.glob(".claude/skills/*/SKILL.md")):
    try:
        d = str(yaml.safe_load(open(f).read().split("\n---\n")[0][4:])["description"]).strip()
    except Exception as e:
        print(f"{f}: frontmatter does not parse: {e}"); bad = 1; continue
    if len(d) > 500: print(f"{f}: description is {len(d)} characters"); bad = 1
    if not d.startswith("This skill should be used"): print(f"{f}: description is not third person"); bad = 1
print("descriptions ok" if not bad else "descriptions FAILED")
sys.exit(bad)
PY
  # Every test file by name, so a new one runs without an edit here; scripts/canary.py proves each goes red.
  say "script tests: every test_*.py, test_*.sh and *.test.sh"
  local pyt=(python3)
  python3 -c 'import hypothesis' 2>/dev/null || ! command -v uv >/dev/null || pyt=(uv run --quiet --no-project --with hypothesis python3)
  local t
  # The list comes on fd 3: a test that reads stdin (ffmpeg does) would swallow the file names after it.
  while IFS= read -r t <&3; do
    [[ -f "$t" && "$t" != tests/claude-owned/* ]] || continue
    if [[ "$t" == *.py ]]; then run "${pyt[@]}" -I "$t"; else run bash "$t"; fi
  done 3< <(git ls-files --cached --others --exclude-standard -- ':(glob)**/test_*.py' ':(glob)**/test_*.sh' ':(glob)**/*.test.sh')
}

# Proves the graders go red: a failing test in every file, rigged copies, decoy mods.
selftest() {
  say "canary: every test file goes red in smoke.sh tests"; run python3 -I scripts/canary.py
  say "canary self-test: a rigged run() and early exits are caught"; run python3 -I scripts/canary.py --self-test
  # Only the summary: the decoys' own ✘ lines are the expected red, not failures.
  say "claude-owned self-test: decoy mods are caught"
  run bash -c "set -o pipefail; python3 tests/claude-owned/run.py --self-test | tail -1"
}

doctor() {
  say "/skill-doctor with the skill plugins installed"; installed
  local ref='op://Personal/Claude Code OAuth token/credential' token="${CLAUDE_CODE_OAUTH_TOKEN:-}"
  if [[ -z "$token" ]] && ! token="$(op read "$ref" 2>&1)"; then
    echo "BLOCKED: CLAUDE_CODE_OAUTH_TOKEN is not set and \`op read '$ref'\` failed: $token"; blocked=1; return
  fi
  local out; out="$(CLAUDE_CODE_OAUTH_TOKEN="$token" CLAUDE_CONFIG_DIR="$cfg" claude -p '/skill-doctor' --max-budget-usd 1 2>&1)"; local st=$?
  if grep -qE 'Not logged in|Failed to authenticate' <<<"$out"; then echo "BLOCKED: the token was refused; run \`claude setup-token\` and save the new token at $ref"; blocked=1; return; fi
  grep -v anthropic-skills <<<"$out"; [[ $st -eq 0 ]] || { failed=1; echo "FAILED: /skill-doctor exit $st"; }
}

details() { say "plugin details"; installed; for p in "${plugins[@]}"; do run env CLAUDE_CONFIG_DIR="$cfg" claude plugin details "$p@dotfiles"; done; }

case "$step" in
  validate|tests|selftest|doctor|details) "$step" ;;
  all) validate; tests; selftest; details; doctor ;;
  *) echo "usage: $0 [validate|tests|selftest|doctor|details|all]" >&2; exit 64 ;;
esac
find plugins -name __pycache__ -prune -exec rm -rf {} +
(( failed )) && exit 1
(( blocked )) && exit 2
exit 0
