#!/usr/bin/env bash
# SessionStart, matcher "compact": a trial of re-injecting focus after a compaction.
# Evidence (hone, 2026-11-16): in two losses the compaction summary already held the fact, and
# Claude still did not act on it. So this points at the summary's newest steer instead of
# adding facts. Half the sessions get it, picked by session id, so a later count of corrections
# after compaction can compare the two halves. Each run logs its arm to compact-trial.log.
# End the trial by removing the hook entry; the log stays.
set -euo pipefail

input="$(cat)"
sid="$(printf '%s' "$input" | jq -r '.session_id // ""')"
cwd="$(printf '%s' "$input" | jq -r '.cwd // ""')"
[ -n "$sid" ] || exit 0

# Arm from the last hex digit of the session id: even gets the text, odd is the control.
last="${sid: -1}"
arm=control
case "$last" in [02468aceACE]) arm=reinject ;; esac

log="${COMPACT_TRIAL_LOG:-$HOME/.claude/hooks/compact-trial.log}"
printf '%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$sid" "$arm" "$cwd" >> "$log" 2>/dev/null || true

[ "$arm" = reinject ] || exit 0

files=""
if [ -n "$cwd" ] && [ -d "$cwd" ]; then
  files="$(find "$cwd" -maxdepth 4 -path '*/node_modules' -prune -o \
    \( -name CHECKPOINT.md -o -name progress.md -o -name PROGRESS.md \) -type f -print 2>/dev/null | head -3)"
fi

text="A compaction just ran. Before your next action:
1. Find the user's newest request and steer in the summary, in their words, and act on that, not on an older plan.
2. Re-read the open items, open PRs and what was checked from where the summary says they are kept."
[ -z "$files" ] || text="$text
3. Re-read: $(printf '%s' "$files" | tr '\n' ' ')"

jq -n --arg t "$text" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$t}}'
