#!/usr/bin/env bash
# PreToolUse hook for mcp__ccd_turn__wrap_up and AskUserQuestion.
# Denies a question that only asks for a go-ahead to commit, push or open a pull request.
# A project that wants a sign-off turns it off with a file: .claude/wants-sign-off.
set -u

input="$(cat)"

root_has_switch() {
  local dir
  for dir in "${CLAUDE_PROJECT_DIR:-}" "$(printf '%s' "$input" | jq -r '.cwd // empty')"; do
    [ -n "$dir" ] && [ -d "$dir" ] || continue
    [ -e "$dir/.claude/wants-sign-off" ] && return 0
    top="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" || continue
    [ -e "$top/.claude/wants-sign-off" ] && return 0
  done
  return 1
}

# Steps that keep their question: merge, force push, delete, history rewrite, production,
# sign-in or secret. A product or design choice does not start with a commit verb.
# "draft": the owner may still change its text. "PR that": an offer of new work.
keep='merge|force|delet|remov|purg|drop|reset|rewrit|histor|deploy|production|prod\b|releas|publish|1password|sign[ -]?in|log[ -]?in|secret|token|unlock|password|credential|api key|draft|(pr|pull request) (that|which) '

# The whole question is a go-ahead: an optional "Shall I" or "Run verify and", then commit,
# push, open a pull request or run create-pr, in one sentence.
go='^((shall|should|may|can|do) i |will you |ok to )?(run (/?verify|the checks) and )?(commit|push|(open|create|make) (a |the |its |this )?([a-z0-9#-]+ )*(pr|pull request)|run /?[a-z:-]*create-pr)\b[^?.!]*\?$'

is_go_ahead() {
  local text
  text="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr '\n' ' ' | sed -E 's/^ +//; s/ +$//')"
  printf '%s' "$text" | grep -Eq "$go" || return 1
  printf '%s' "$text" | grep -Eq "$keep" && return 1
  return 0
}

tool="$(printf '%s' "$input" | jq -r '.tool_name // empty')"
deny=0

case "$tool" in
  AskUserQuestion)
    count="$(printf '%s' "$input" | jq -r '.tool_input.questions // [] | length')"
    if [ "$count" -gt 0 ]; then
      deny=1
      while IFS= read -r q; do
        is_go_ahead "$q" || deny=0
      done < <(printf '%s' "$input" | jq -r '.tool_input.questions[].question | gsub("\n"; " ")')
    fi
    next="Do the step by the commit flow in the global rules, then say in your report what you committed, pushed or opened."
    ;;
  *wrap_up)
    ask="$(printf '%s' "$input" | jq -r '.tool_input.ask // empty')"
    if [ -n "$ask" ]; then
      everything="$(printf '%s' "$input" | jq -r '[.tool_input.ask, (.tool_input.actions // [] | .[] | .label // empty)] | join(" ")' | tr '[:upper:]' '[:lower:]')"
      if printf '%s' "$input" | jq -e '[.tool_input.actions // [] | .[] | .action] | any(. == "commit" or . == "create_pr")' >/dev/null; then
        printf '%s' "$everything" | grep -Eq "$keep" || deny=1
      fi
      is_go_ahead "$ask" && deny=1
    fi
    next="Do the step by the commit flow in the global rules, then call wrap_up again with the recap and no ask."
    ;;
esac

if [ "$deny" -eq 1 ] && ! root_has_switch; then
  reason="Question blocked by ~/.claude/hooks/deny-go-ahead-questions.sh: it only asks for a go-ahead to commit, push or open a pull request. The commit flow in the global rules is a standing order, so the owner has already said yes. $next A merge, a force push, a delete, a production change, a sign-in or a secret still gets its question. A project that wants a sign-off adds the file .claude/wants-sign-off."
  jq -n --arg r "$reason" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
fi

exit 0
