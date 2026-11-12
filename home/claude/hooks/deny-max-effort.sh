#!/usr/bin/env bash
# PreToolUse hook: deny a subagent or thread start with effort `max`.
# It checks only the effort field of the call; the session's own /effort setting stays the owner's.

set -u

input="$(cat)"

effort="$(printf '%s' "$input" | jq -r '.tool_input.effort // empty | ascii_downcase | gsub("^\\s+|\\s+$"; "")')"

if [ "$effort" = "max" ]; then
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Effort `max` is blocked by ~/.claude/hooks/deny-max-effort.sh. Start the work again at `high`, or at `xhigh` if `high` already failed. On Artificial Analysis, max costs about 1.5 to 3 times xhigh for 1 to 5 more index points and waits minutes for the first token; on code-review benchmarks it raised false findings. Remove the hook to override."}}
JSON
fi

exit 0
