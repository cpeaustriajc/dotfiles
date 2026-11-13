#!/usr/bin/env bash
# PreToolUse hook for mcp__ccd_turn__wrap_up and AskUserQuestion.
# Denies a question that only asks for a go-ahead to commit, push or open a pull request.
# It denies a question once: an agent with a real reason asks it again soon after, and the second
# time it goes through. A project that wants a sign-off turns the hook off with a
# file: .claude/wants-sign-off.
# Failure: agents asked the owner to approve work the owner had already asked for.
set -u

input="$(cat)"
sep=$'\x1f'
# The plain fields, in one jq call. A missing field is "".
IFS="$sep" read -r tool session cwd < <(printf '%s' "$input" | jq -r '[.tool_name, .session_id, .cwd] | map(. // "" | tostring) | join("\u001f")' 2>/dev/null)

# The switch counts in the cwd or CLAUDE_PROJECT_DIR, in any folder above them, and in the main
# checkout of a worktree.
root_has_switch() {
  local dir d common
  for dir in "${CLAUDE_PROJECT_DIR:-}" "$cwd"; do
    [ -n "$dir" ] && [ -d "$dir" ] || continue
    d="$dir"
    while :; do
      [ -e "$d/.claude/wants-sign-off" ] && return 0
      [ "$d" = / ] || [ "$d" = . ] && break
      d="$(dirname "$d")"
    done
    common="$(git -C "$dir" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" || continue
    [ "$(basename "$common")" = .git ] && [ -e "$(dirname "$common")/.claude/wants-sign-off" ] && return 0
  done
  return 1
}

# A go-ahead question has a fixed shape: an optional opening, then one or more steps joined by
# "and", each with only object and target words after it. Any other word makes it a real
# question, so a new phrasing is let through (a missed block) instead of blocked by mistake.
# "Will you" is left out: it asks the owner to do the step. "Run verify" counts only before a
# commit, push or PR step. "Open a docs PR" has a word before "PR", so it is an offer of a new
# PR and not a go-ahead.
opening='((shall|should|may|can|could|do) (i|we) |(do you )?want me to |would you like me to |(is it )?ok to |go ahead and )?((run )?(/?verify|the checks) and )?'
step='(commit|push|(open|create) (a |the |its |this )?(pr|pull request)|run /?[a-z:-]*create-pr)'
# Object words, from a fixed list only: no free word may stand before a noun, so "the
# sensitive files" or "just the docs" do not fit. Nouns may follow each other ("the README
# commit").
noun='(commits?|changes?|fix|fixes|work|branch|skill|docs?|readme|rules?|tests?|files?|dotfiles|style)'
object="(the|this|these|that|it|them|its|my|both|all|a|an|and|now|for|[0-9]+|two|three|four|five|six|[0-9a-f]{7,40}|#[0-9]+|$noun|pr|main)"
# Targets: only the usual ones may follow "to", "into" or "on". Another target is a choice.
target="(to|into|on) (the )?(main|master|origin( main)?|github|upstream|remote|pr( #?[0-9]+)?|#[0-9]+|(origin|upstream|claude|feat|fix|chore|docs)/[a-z0-9._/-]+)|to open (the |a )?(pr|pull request)"
clause="$opening$step( ($object|$target))*"
go="^$clause( and $clause)*\\?\$"

# Words that keep the question even in the go-ahead shape, or in an option label, header or
# recap: a merge, a force push, a delete, a production change, a sign-in or secret, a skipped
# hook, a failed or blocked step, a doubt, private or unfinished content, an open draft. The
# list cannot be complete; the deny-once rule above covers what it misses.
keep='merge|\bforce|-f\b|\brebas|\boverwrit|\brevert|\bdelet|\bremov|\bdrop|\bwipe|\bdestroy|\btruncat|\bpurg|\breset|\brewrit|\bhistory|\bsquash|--hard|\bdeploy|production|\bprod\b|\breleas|\bpublish|1password|sign[ -]?in|log[ -]?in|\bauth|secret|\btokens?\b|unlock|password|credential|api key|private key|ssh key|\.env\b|no-verify|\bamend|\bfail|\breject|\berror|\bwarning|\bdenied|conflict|protect|\banyway|\bblocked|cannot|can.t|unable|could ?n.t|untested|unsure|not sure|unclear|unrelated|unexpected|someone else|\brisk|irreversib|diverged|\b(401|403|404|409|422|500|502|503)\b|\bprivate|personal|customer|\bwip\b|broken|experiment|half|draft'

# An option label that only declines. It must be the whole label, so "No, push to a feature
# branch" counts as a real choice.
decline='^(no|no,? thanks|nope|not (right )?(now|yet)|later|leave it|keep it|hold( it)?|wait|skip|cancel|negative)\.?$'
# An option label that only says yes: a yes word, or a step in the go-ahead shape, with or
# without "Yes," before it ("Yes, push"). "Open a PR instead" is neither, so it is a choice.
yes='^(yes|ok|okay|affirm|sure|do it|go ahead|create_pr|commit)\.?$'

has() { printf '%s' "$2" | grep -Eq "$1"; }

says_yes() {
  local label="${1#yes, }"
  has "$yes" "$label" || has "$go" "$label?"
}

# $1: one row. Field 0 is the question, field 1 the recap, the rest are options. Lower case.
is_go_ahead() {
  local f i yeses=0
  IFS="$sep" read -r -a f <<< "$1$sep"
  has "$go" "${f[0]}" || return 1
  ! has "$keep" "${f[*]}" || return 1
  # Each option declines or says yes, and only one says yes: two yes labels ("Push to origin",
  # "Push to upstream") are a choice for the owner.
  for ((i = 2; i < ${#f[@]}; i++)); do
    has "$decline" "${f[i]}" && continue
    says_yes "${f[i]}" || return 1
    yeses=$((yeses + 1))
  done
  [ "$yeses" -le 1 ]
}

# One row per question, with fields split by the unit separator (not white space, so an empty
# field stays a field): the question, the recap (for a card: its header), then each option
# label, with the "(Recommended)" mark that the card guide adds taken off. For wrap_up, the recap field also holds each button's action name, so the keep words see
# a merge or deploy button. A multi-select card, or an option with a description or preview, offers a choice, so
# that card question is sent as "" and never matches. A jq error lets the question through.
rows="$(printf '%s' "$input" | jq -r '
  def flat: ascii_downcase | gsub("\\s+"; " ") | ltrimstr(" ") | rtrimstr(" ");
  if .tool_name == "AskUserQuestion" then
    .tool_input.questions[]?
    | [(if .multiSelect == true or any(.options[]?; (.description // "") != "" or (.preview // "") != "") then "" else .question // "" | flat end), (.header // "" | flat)]
      + [.options[]? | .label // "" | flat | sub(" \\(recommended\\)$"; "")] | join("\u001f")
  elif (.tool_name // "" | endswith("wrap_up")) and (.tool_input.ask // "") != "" then
    [(.tool_input.ask | flat), ([.tool_input.recap // ""] + [.tool_input.actions[]? | .action // "" | tostring] | join(" ") | flat)] + [.tool_input.actions[]? | .label // "" | flat | sub(" \\(recommended\\)$"; "")] | join("\u001f")
  else empty end' 2>/dev/null)" || exit 0

# Deny only when every question is a go-ahead.
[ -n "$rows" ] || exit 0
while IFS= read -r row; do
  is_go_ahead "$row" || exit 0
done <<< "$rows"
root_has_switch && exit 0

# Deny once: the next go-ahead in this session within the window after a deny goes through, in any
# words, so an agent with a real question can ask it again. That re-ask uses up the deny, so a
# go-ahead after it is denied again. Without a session id, or without a place to record the deny,
# let it through: a deny that cannot be recorded would repeat on every ask.
session="${session//[^a-zA-Z0-9-]/_}"
state="${TMPDIR:-/tmp}/deny-go-ahead-questions"
window=600 now="$(date +%s)"
last="$(cat "$state/$session" 2>/dev/null)"
if [ -n "$last" ] && [ $((now - last)) -lt "$window" ]; then
  rm -f "$state/$session"
  exit 0
fi
{ mkdir -p "$state" && printf '%s\n' "$now" > "$state/$session"; } 2>/dev/null || exit 0

case "$tool" in
  AskUserQuestion) next="Do the step by the commit flow in the global rules, then say in your report what you committed, pushed or opened." ;;
  *) next="Do the step by the commit flow in the global rules, then call wrap_up again with the recap and no ask." ;;
esac
reason="Question blocked by ~/.claude/hooks/deny-go-ahead-questions.sh: it only asks for a go-ahead to commit, push or open a pull request. The commit flow in the global rules is a standing order, so the owner has already said yes. $next If the step fails, ask again and name the error. If this is a real question (a doubt about the work, a blocker, a choice of target or scope, or a project rule that requires a sign-off or forbids the step), do not do the step: ask the same question again within $((window / 60)) minutes, and it goes through. The file .claude/wants-sign-off turns this hook off for a project."
jq -n --arg r "$reason" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
