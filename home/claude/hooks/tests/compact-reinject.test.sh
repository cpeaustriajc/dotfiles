#!/usr/bin/env bash
# One case for each way compact-reinject.sh can fail. Run: bash home/claude/hooks/tests/compact-reinject.test.sh
set -u
hook="$(cd "$(dirname "$0")/.." && pwd)/compact-reinject.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export COMPACT_TRIAL_LOG="$tmp/trial.log"
pass=0 fail=0

# run <name> <session_id> <cwd> <jq test on the output, or "empty">
run() {
  local name="$1" sid="$2" cwd="$3" want="$4" out ok=0
  out="$(jq -n --arg s "$sid" --arg c "$cwd" '{session_id:$s,cwd:$c,hook_event_name:"SessionStart",source:"compact"}' | bash "$hook")"
  if [ "$want" = empty ]; then [ -z "$out" ] && ok=1
  else printf '%s' "$out" | jq -e "$want" >/dev/null 2>&1 && ok=1; fi
  if [ "$ok" = 1 ]; then pass=$((pass + 1)); else fail=$((fail + 1)); echo "FAIL $name: got '$out'"; fi
}

mkdir -p "$tmp/repo/.claude/work/x" "$tmp/bare"
touch "$tmp/repo/.claude/work/x/CHECKPOINT.md"

run "even id gets the text" "022bf50b-0000-0000-0000-000000000000" "$tmp/bare" \
  '.hookSpecificOutput.additionalContext | test("newest request")'
run "odd id is the control" "03c808d2-0000-0000-0000-000000000001" "$tmp/bare" empty
run "names a checkpoint file" "aa-2" "$tmp/repo" \
  '.hookSpecificOutput.additionalContext | test("CHECKPOINT.md")'
run "no checkpoint, no step 3" "aa-4" "$tmp/bare" \
  '.hookSpecificOutput.additionalContext | test("Re-read:") | not'
run "missing session id is silent" "" "$tmp/bare" empty

lines="$(wc -l < "$COMPACT_TRIAL_LOG" | tr -d ' ')"
if [ "$lines" = 4 ] && grep -q $'\tcontrol\t' "$COMPACT_TRIAL_LOG" && grep -q $'\treinject\t' "$COMPACT_TRIAL_LOG"; then
  pass=$((pass + 1))
else
  fail=$((fail + 1)); echo "FAIL log: want 4 lines with both arms, got $lines"
fi

echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
