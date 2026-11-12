#!/usr/bin/env bash
# One case for each way deny-go-ahead-questions.sh can fail. Run: bash home/claude/hooks/tests/deny-go-ahead-questions.test.sh
set -u
hook="$(cd "$(dirname "$0")/.." && pwd)/deny-go-ahead-questions.sh"
plain="$(mktemp -d)"
pass=0 fail=0

# run <want: deny|allow> <name> <tool_input JSON> [cwd] [CLAUDE_PROJECT_DIR]
run() {
  local want="$1" name="$2" tool="$3" ti="$4" cwd="${5:-$plain}" pdir="${6:-}" out got
  out="$(jq -n --arg t "$tool" --argjson ti "$ti" --arg c "$cwd" '{tool_name:$t,tool_input:$ti,cwd:$c}' \
    | env -u CLAUDE_PROJECT_DIR ${pdir:+CLAUDE_PROJECT_DIR="$pdir"} bash "$hook")"
  got=allow
  if [ -n "$out" ]; then
    printf '%s' "$out" | jq -e '.hookSpecificOutput.permissionDecision == "deny"' >/dev/null && got=deny || got=bad-json
  fi
  if [ "$got" = "$want" ]; then pass=$((pass + 1)); else fail=$((fail + 1)); echo "FAIL $name: want $want, got $got"; fi
}
wrap() { jq -n --arg a "$1" --argjson acts "${2:-[]}" --argjson b "${3:-false}" '{recap:"Did the work.",ask:$a,actions:$acts,blocked:$b}'; }
ask() { jq -n --arg q "$1" '{questions:[{question:$q,header:"Go",options:[{label:"Yes"},{label:"Not now"}],multiSelect:false}]}'; }
W=mcp__ccd_turn__wrap_up A=AskUserQuestion

# Go-ahead questions that the hook denies.
run deny "create_pr button" $W "$(wrap 'Ready for review?' '[{"label":"Open PR","action":"create_pr"},{"label":"Not now"}]')"
run deny "commit button" $W "$(wrap 'Anything else?' '[{"label":"Commit","action":"commit"}]')"
run deny "push a sha to main" $W "$(wrap 'Push a1b2c3d to main?')"
run deny "shall I open the PR" $W "$(wrap 'Shall I open the pull request for this branch?')"
run deny "run verify and commit" $W "$(wrap 'Run verify and commit the rule change?')"
run deny "upper case and line break" $W "$(wrap $'PUSH THE TWO\nCOMMITS?')"
run deny "will you run create-pr" $W "$(wrap 'Will you run /engineering:create-pr to open the PR?')"
run deny "blocked:true is no real block" $W "$(wrap 'Push the branch and open the PR?' '[]' true)"
run deny "question card go-ahead" $A "$(ask 'Push the 3 commits to main?')"
run deny "every card question is a go-ahead" $A '{"questions":[{"question":"Commit the fix?","header":"a","options":[],"multiSelect":false},{"question":"Push it?","header":"b","options":[],"multiSelect":false}]}'

# Questions that keep their place.
run allow "merge" $W "$(wrap 'Push and merge PR 12?')"
run allow "merge label next to create_pr" $W "$(wrap 'Ship it?' '[{"label":"Open PR and merge","action":"create_pr"}]')"
run allow "force push" $W "$(wrap 'Push the rebased branch with --force-with-lease?')"
run allow "delete" $W "$(wrap 'Push the cleanup that deletes 40 remote branches?')"
run allow "production" $W "$(wrap 'Push to main, which deploys to production?')"
run allow "sign-in or secret" $W "$(wrap 'Unlock 1Password so the push can go?')"
run allow "history rewrite" $W "$(wrap 'Commit the history rewrite that drops node_modules?')"
run allow "draft text still open" $W "$(wrap 'Commit the draft at 1,400 characters?')"
run allow "offer of a new PR" $W "$(wrap 'Shall I open a docs PR that makes the rules match?')"
run allow "product choice" $W "$(wrap 'Which accent colour should the app use?')"
run allow "choice of branch" $W "$(wrap 'Where do I commit this change?')"
run allow "extra work before push" $W "$(wrap 'Fix the two lines too before the push?')"
run allow "long question with an example" $A "$(ask "Push the stack in which order? Example: #12 changes the schema and #13 reads it, so #13 fails on its own if it lands first, and the reader sees a broken page for one deploy.")"
run allow "card mixes go-ahead and design" $A '{"questions":[{"question":"Commit the fix?","header":"a","options":[],"multiSelect":false},{"question":"Which layout?","header":"b","options":[],"multiSelect":false}]}'
run allow "recap with no ask" $W '{"recap":"Pushed a1b2c3d."}'
run allow "other tool" Bash '{"command":"git push"}'

# The project switch.
proj="$(mktemp -d)"; git -C "$proj" init -q; mkdir -p "$proj/.claude" "$proj/sub/dir"; touch "$proj/.claude/wants-sign-off"
run allow "switch in cwd" $W "$(wrap 'Push a1b2c3d to main?')" "$proj"
run allow "switch at git root of a subfolder" $W "$(wrap 'Push a1b2c3d to main?')" "$proj/sub/dir"
run allow "switch in CLAUDE_PROJECT_DIR" $W "$(wrap 'Push a1b2c3d to main?')" "$plain" "$proj"
run deny "missing cwd folder" $W "$(wrap 'Push a1b2c3d to main?')" "$plain/gone"

# The deny reason names the next action.
reason="$(wrap 'Push a1b2c3d to main?' | jq -n --argjson ti "$(cat)" '{tool_name:"mcp__ccd_turn__wrap_up",tool_input:$ti}' | env -u CLAUDE_PROJECT_DIR bash "$hook" | jq -r '.hookSpecificOutput.permissionDecisionReason')"
case "$reason" in *"call wrap_up again with the recap and no ask"*".claude/wants-sign-off"*) pass=$((pass + 1)) ;; *) fail=$((fail + 1)); echo "FAIL wrap_up reason: $reason" ;; esac

rm -rf "$plain" "$proj"
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
