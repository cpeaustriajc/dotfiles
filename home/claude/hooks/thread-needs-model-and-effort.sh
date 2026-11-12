#!/usr/bin/env bash
set -u

input="$(cat)"

prompt="$(printf '%s' "$input" | jq -r '.tool_input.prompt // empty')"
model="$(printf '%s' "$input" | jq -r '.tool_input.model // empty')"
effort="$(printf '%s' "$input" | jq -r '.tool_input.effort // empty')"

if [ -n "$prompt" ] && { [ -z "$model" ] || [ -z "$effort" ]; }; then
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Thread start blocked by ~/.claude/hooks/thread-needs-model-and-effort.sh: start_session needs both `model` and `effort`. Without a model the thread inherits the default, opus[1m]. This hook checks only that both are set; the choice is yours. The \"Claude Code\" part of the global rules says how to choose."}}
JSON
fi

exit 0
