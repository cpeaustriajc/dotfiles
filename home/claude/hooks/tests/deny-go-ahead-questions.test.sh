#!/usr/bin/env bash
# One case for each way deny-go-ahead-questions.sh can fail. Run: bash home/claude/hooks/tests/deny-go-ahead-questions.test.sh
set -u
hook="$(cd "$(dirname "$0")/.." && pwd)/deny-go-ahead-questions.sh"
base="$(mktemp -d)"
trap 'chmod -R u+w "$base"; rm -rf "$base"' EXIT
plain="$base/plain"; mkdir "$plain"
pass=0 fail=0

# run <want: deny|allow> <name> <tool_input JSON> [cwd] [CLAUDE_PROJECT_DIR]
# Each run gets its own state folder, so the deny-once state of one case does not reach the next.
run() {
  local want="$1" name="$2" tool="$3" ti="$4" cwd="${5:-$plain}" pdir="${6:-}" out got
  out="$(jq -n --arg t "$tool" --argjson ti "$ti" --arg c "$cwd" '{tool_name:$t,session_id:"test",tool_input:$ti,cwd:$c}' \
    | env -u CLAUDE_PROJECT_DIR TMPDIR="$(mktemp -d "$base/state.XXXXXX")" ${pdir:+CLAUDE_PROJECT_DIR="$pdir"} bash "$hook")"
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
run deny "go-ahead next to a create_pr button" $W "$(wrap 'Open the PR for this branch?' '[{"label":"Open PR","action":"create_pr"},{"label":"Not now"}]')"
run deny "push a sha to main" $W "$(wrap 'Push a1b2c3d to main?')"
run deny "shall I open the PR" $W "$(wrap 'Shall I open the pull request for this branch?')"
run deny "run verify and commit" $W "$(wrap 'Run verify and commit the rule change?')"
run deny "upper case and line break" $W "$(wrap $'PUSH THE TWO\nCOMMITS?')"
run deny "run create-pr to open the PR" $W "$(wrap 'Shall I run /engineering:create-pr to open the PR?')"
run allow "will you: the owner is asked to do the step" $W "$(wrap 'Will you run /engineering:create-pr to open the PR?')"
run deny "blocked:true is no real block" $W "$(wrap 'Push the branch and open the PR?' '[]' true)"
run deny "question card go-ahead" $A "$(ask 'Push the 3 commits to main?')"
run deny "every card question is a go-ahead" $A '{"questions":[{"question":"Commit the fix?","header":"a","options":[],"multiSelect":false},{"question":"Push it?","header":"b","options":[],"multiSelect":false}]}'
run deny "a (Recommended) yes label" $A '{"questions":[{"question":"Commit and push to main?","header":"Ship","options":[{"label":"Yes (Recommended)"},{"label":"No, thanks"}],"multiSelect":false}]}'
run deny "a (Recommended) yes button in wrap_up" $W "$(wrap 'Push to main?' '[{"label":"Yes (Recommended)"},{"label":"Not now"}]')"
run deny "more decline labels" $A '{"questions":[{"question":"Push it?","header":"Ship","options":[{"label":"Yes"},{"label":"Nope"},{"label":"Not right now"},{"label":"No thanks"}],"multiSelect":false}]}'

# Questions that keep their place.
run allow "a doubt about unrelated changes" $W "$(jq -n '{recap:"The staged diff also has unrelated changes.",ask:"Commit the changes?"}')"
run allow "not sure in the recap" $W "$(jq -n '{recap:"Not sure these files belong here.",ask:"Commit the files?"}')"
run allow "a merge button behind a yes label" $W "$(wrap 'Push to main?' '[{"label":"Yes","action":"merge_pr"}]')"
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
run deny "do you want me to" $W "$(wrap 'Do you want me to commit and push?')"
run deny "would you like me to" $A "$(ask 'Would you like me to open the PR?')"
run deny "a recap word that only holds a keep word" $W '{"recap":"Enforced the lint rules.","ask":"Push a1b2c3d to main?"}'
run allow "commit button next to a real choice" $W "$(wrap 'Which cache approach?' '[{"label":"Commit","action":"commit"}]')"
run allow "commit button next to a design question" $W "$(wrap 'Is the layout right?' '[{"label":"Commit","action":"commit"}]')"
run allow "create_pr button alone" $W "$(wrap 'Ready for review?' '[{"label":"Open PR","action":"create_pr"}]')"
run allow "keep word after a line break in a card" $A "$(ask $'Push the cleanup that\ndeletes old branches?')"
run allow "choice of target" $W "$(wrap 'Commit to main or a new branch?')"
run allow "choice of remote" $W "$(wrap 'Push to origin or to your fork?')"
run allow "choice in the option labels" $A '{"questions":[{"question":"Push the commits?","header":"a","options":[{"label":"Push to main"},{"label":"Push to a new branch"}],"multiSelect":false}]}'
run allow "keep word in an option description" $A '{"questions":[{"question":"Push it?","header":"a","options":[{"label":"Yes","description":"Deploys to production"}],"multiSelect":false}]}'
run allow "skip the git hooks" $W "$(wrap 'Commit with --no-verify?')"
run allow "amend" $W "$(wrap 'Push after I amend the commit?')"
run allow "secret file" $W "$(wrap 'Commit the .env file?')"
run allow "a failed step" $W "$(wrap 'Push again? Branch protection rejected the last push.')"
run allow "a failed step in one sentence" $W "$(wrap 'Push again after the rejected push?')"
run allow "rebased branch needs a force push" $W "$(wrap 'Push the rebased branch?')"
run allow "short force flag" $W "$(wrap 'Push with -f?')"
run allow "a delete in another verb form" $W "$(wrap 'Push the migration that drops the users table?')"
run allow "push past a problem" $W "$(wrap 'Push anyway?')"
run allow "failure only in the recap" $W '{"recap":"3 tests failed.","ask":"Push a1b2c3d to main?"}'
run allow "two real options" $A '{"questions":[{"question":"Commit the changes?","header":"a","options":[{"label":"One commit"},{"label":"Two commits"}],"multiSelect":false}]}'
run allow "new work joined to the step" $W "$(wrap 'Commit the fix and start the next ticket?')"
run allow "purpose clause" $W "$(wrap 'Push main so the docs site updates?')"
run allow "empty question with a go-ahead option" $A '{"questions":[{"question":"","header":"a","options":[{"label":"Push it?"}],"multiSelect":false}]}'
run deny "two objects joined by and" $W "$(wrap 'Push main and the docs?')"
run allow "a hyphenated phrase is a free word" $W "$(wrap 'Push the output-style commits?')"
run allow "a decline label that offers another step" $A '{"questions":[{"question":"Push to main?","header":"a","options":[{"label":"Yes"},{"label":"No, push to a feature branch"}],"multiSelect":false}]}'
run allow "a card option with a description explains a choice" $A '{"questions":[{"question":"Push to main?","header":"a","options":[{"label":"Yes"},{"label":"Not now","description":"Keep it local"}],"multiSelect":false}]}'
run deny "yes and a decline" $A '{"questions":[{"question":"Push to main?","header":"a","options":[{"label":"Yes"},{"label":"Not now"}],"multiSelect":false}]}'
run deny "a label that names the step" $W "$(wrap 'Push a1b2c3d to main?' '[{"label":"Yes, push"},{"label":"Not yet"}]')"
run allow "one label that offers another step" $A '{"questions":[{"question":"Push the commits?","header":"a","options":[{"label":"Open a PR instead"},{"label":"No"}],"multiSelect":false}]}'
run allow "skip the checks" $W "$(wrap 'Commit without running tests?')"
run allow "part of the work" $W "$(wrap 'Commit just the docs?')"
run allow "a word before a noun" $W "$(wrap 'Commit the sensitive files?')"
run allow "either target" $W "$(wrap 'Commit to main or a branch?')"
run allow "a hyphenated word alone" $W "$(wrap 'Commit the work-in-progress?')"
run allow "a slash between two targets" $W "$(wrap 'Commit to main/develop?')"
run deny "a branch path target" $W "$(wrap 'Push to claude/fix-563?')"
run deny "verify and commit" $W "$(wrap 'Verify and commit the fix?')"
run allow "private content" $W "$(wrap 'Commit the customer data files?')"
run allow "unfinished content" $W "$(wrap 'Commit the half-finished work?')"
run allow "offer of a second PR" $W "$(wrap 'Open a docs PR?')"
run allow "a doubt in the recap" $W '{"recap":"Unsure about rounding; untested.","ask":"Push to main?"}'
run allow "a blocker in the recap" $W '{"recap":"Push got a 403 from origin.","ask":"Push a1b2c3d to main?"}'
run allow "the checks alone" $W "$(wrap 'Run the checks?')"
run allow "an unusual target" $W "$(wrap 'Push to the live-server?')"
run allow "a question that is not a string" $A '{"questions":[{"question":"Push it?","header":"a","options":[],"multiSelect":false},{"question":42,"header":"b","options":[],"multiSelect":false}]}'
run allow "a multi-select card" $A '{"questions":[{"question":"Commit and push?","header":"a","options":[{"label":"Push to main"},{"label":"No"}],"multiSelect":true}]}'
run allow "an option with a preview" $A '{"questions":[{"question":"Push to main?","header":"a","options":[{"label":"Yes","preview":"git push origin main"},{"label":"No"}],"multiSelect":false}]}'
run allow "a keep word in the card header" $A '{"questions":[{"question":"Push to main?","header":"Force or normal","options":[{"label":"Yes"},{"label":"No"}],"multiSelect":false}]}'
run allow "two yes labels with different targets" $W "$(wrap 'Push to origin?' '[{"label":"Push to origin"},{"label":"Push to upstream"}]')"
run allow "recap with no ask" $W '{"recap":"Pushed a1b2c3d."}'
run allow "other tool" Bash '{"command":"git push"}'

# The project switch. Every folder sits in $base, which holds no switch itself.
proj="$base/proj"; mkdir -p "$proj/.claude" "$proj/sub/dir"; git -C "$proj" init -q; touch "$proj/.claude/wants-sign-off"
run allow "switch in cwd" $W "$(wrap 'Push a1b2c3d to main?')" "$proj"
run allow "switch at git root of a subfolder" $W "$(wrap 'Push a1b2c3d to main?')" "$proj/sub/dir"
run allow "switch in CLAUDE_PROJECT_DIR" $W "$(wrap 'Push a1b2c3d to main?')" "$plain" "$proj"
wt="$base/wt"; git -C "$proj" commit -q --allow-empty -m init; git -C "$proj" worktree add -q "$wt"
run allow "switch in the main checkout of a worktree" $W "$(wrap 'Push a1b2c3d to main?')" "$wt"
bare="$base/bare"; bwt="$base/bare-wt"; git clone -q --bare "$proj" "$bare/repo.git"; git -C "$bare/repo.git" worktree add -q "$bwt" 2>/dev/null; mkdir -p "$bare/.claude"; touch "$bare/.claude/wants-sign-off"
run deny "a bare repo's parent folder is no checkout" $W "$(wrap 'Push a1b2c3d to main?')" "$bwt"
nogit="$base/nogit"; mkdir -p "$nogit/.claude" "$nogit/src"; touch "$nogit/.claude/wants-sign-off"
run allow "switch in a folder above a cwd outside git" $W "$(wrap 'Push a1b2c3d to main?')" "$nogit/src"
run deny "missing cwd folder" $W "$(wrap 'Push a1b2c3d to main?')" "$plain/gone"

# Deny once: the next go-ahead in the same session, in any words, goes through.
# ask_once <state folder> <session id or ""> <recap> [ask]
ask_once() {
  jq -n --arg s "$2" --arg r "$3" --arg a "${4:-Push a1b2c3d to main?}" '{tool_name:"mcp__ccd_turn__wrap_up",tool_input:{recap:$r,ask:$a}} + (if $s == "" then {} else {session_id:$s} end)' \
    | env -u CLAUDE_PROJECT_DIR TMPDIR="$1" bash "$hook" 2>/dev/null | grep -q '"deny"' && echo deny || echo allow
}
expect() { if [ "$2" = "$3" ]; then pass=$((pass + 1)); else fail=$((fail + 1)); echo "FAIL $1: want '$3', got '$2'"; fi; }
once="$base/once"; mkdir "$once"
expect "deny once per session, and a re-ask uses up the deny" "$(ask_once "$once" s1 x) $(ask_once "$once" s1 x) $(ask_once "$once" s1 x) $(ask_once "$once" s2 x)" "deny allow deny deny"
expect "a re-ask with a new recap" "$(ask_once "$once" s3 x) $(ask_once "$once" s3 'Need your call: the rules say sign-off.')" "deny allow"
expect "a re-ask in new words" "$(ask_once "$once" s10 x) $(ask_once "$once" s10 x 'Shall I push a1b2c3d to main now?')" "deny allow"
# seed <session> <seconds ago>: write a deny time to the state that the hook reads.
old="$base/old"; mkdir -p "$old/deny-go-ahead-questions"
now="$(date +%s)"
seed() { printf '%s\n' "$((now - $2))" > "$old/deny-go-ahead-questions/$1"; }
seed s6 99999
seed s8 300
seed s9 700
expect "a deny from long ago" "$(ask_once "$old" s6 x) $(ask_once "$old" s6 x)" "deny allow"
expect "a re-ask 5 minutes after the deny" "$(ask_once "$old" s8 x)" "allow"
expect "a re-ask 12 minutes after the deny" "$(ask_once "$old" s9 x)" "deny"
expect "no session id" "$(ask_once "$once" "" x)" "allow"
locked="$base/locked"; mkdir "$locked"; chmod 555 "$locked"
expect "a state folder that cannot be written" "$(ask_once "$locked" s4 x) $(ask_once "$locked" s4 x)" "allow allow"
expect "a state folder that cannot be written prints no error" "$(printf '%s' '{"tool_name":"mcp__ccd_turn__wrap_up","session_id":"s5","tool_input":{"recap":"x","ask":"Push a1b2c3d to main?"}}' | env -u CLAUDE_PROJECT_DIR TMPDIR="$locked" bash "$hook" 2>&1 >/dev/null)" ""
chmod 755 "$locked"
expect "a jq error prints nothing" "$(printf '%s' '{"tool_name":"AskUserQuestion","session_id":"e","tool_input":{"questions":[{"question":42}]}}' | env -u CLAUDE_PROJECT_DIR TMPDIR="$once" bash "$hook" 2>&1)" ""

# The deny reason names the next action.
reason="$(wrap 'Push a1b2c3d to main?' | jq -n --argjson ti "$(cat)" '{tool_name:"mcp__ccd_turn__wrap_up",session_id:"r",tool_input:$ti}' | env -u CLAUDE_PROJECT_DIR TMPDIR="$(mktemp -d "$base/state.XXXXXX")" bash "$hook" | jq -r '.hookSpecificOutput.permissionDecisionReason')"
case "$reason" in *"call wrap_up again with the recap and no ask"*"name the error"*"ask the same question again within 10 minutes"*".claude/wants-sign-off"*) pass=$((pass + 1)) ;; *) fail=$((fail + 1)); echo "FAIL wrap_up reason: $reason" ;; esac

echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
