#!/usr/bin/env bash
# One case for each way deny-max-effort.sh can fail. Run: bash home/claude/hooks/tests/deny-max-effort.test.sh
set -u
hook="$(cd "$(dirname "$0")/.." && pwd)/deny-max-effort.sh"
pass=0 fail=0

# run <want: deny|allow> <name> <tool_name> <tool_input JSON>
run() {
  local want="$1" name="$2" tool="$3" ti="$4" out got
  out="$(jq -n --arg t "$tool" --argjson ti "$ti" '{tool_name:$t,session_id:"test",tool_input:$ti}' | bash "$hook")"
  got=allow
  if [ -n "$out" ]; then
    printf '%s' "$out" | jq -e '.hookSpecificOutput.permissionDecision == "deny"' >/dev/null && got=deny || got=bad-json
  fi
  if [ "$got" = "$want" ]; then pass=$((pass + 1)); else fail=$((fail + 1)); echo "FAIL $name: want $want, got $got"; fi
}
S=mcp__ccd_session__start_session

run deny "subagent at max" Agent '{"prompt":"Review it.","model":"sonnet","effort":"max"}'
run deny "legacy Task tool at max" Task '{"prompt":"Review it.","effort":"max"}'
run deny "thread at max" $S '{"prompt":"Build it.","model":"opus","effort":"max"}'
run deny "upper case and spaces" Agent '{"prompt":"Review it.","effort":" MAX "}'
run allow "xhigh stays allowed" Agent '{"prompt":"Review it.","effort":"xhigh"}'
run allow "high" $S '{"prompt":"Build it.","model":"sonnet","effort":"high"}'
run allow "no effort set" Agent '{"prompt":"Review it."}'
run allow "max only in the prompt text" Agent '{"prompt":"Do not use max effort.","effort":"medium"}'
run allow "max as a model name part" Agent '{"prompt":"Review it.","model":"max-model","effort":"low"}'

echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
