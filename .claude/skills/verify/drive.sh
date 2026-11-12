#!/usr/bin/env bash
# Runs feature<TAB>command lines from stdin, one log each, and prints one result line per feature.
# Usage: drive.sh [log root] [base]. Pass the session's scratchpad; the default is under $TMPDIR.
# Each command also runs in a clean clone of the base commit (default: merge-base with origin/main),
# and results.py judges the two logs: exit 0 alone is not a pass.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cd "$(git rev-parse --show-toplevel)"
dir="${1:-${TMPDIR:-/tmp}/claude-verify-$(basename "$PWD")}/$(git rev-parse --short HEAD)"
mkdir -p "$dir"
rows=()
while IFS= read -r row; do [[ "$row" == *$'\t'* ]] && rows+=("$row"); done
total=${#rows[@]}
(( total )) || { echo "no features selected"; exit 0; }

# A fresh clone each run, so no earlier file sets the floor. It shares objects with this repo and
# writes nothing into its .git.
base_dir=""
if sha="$(git merge-base HEAD "${2:-origin/main}" 2>/dev/null)"; then
  base_dir="$dir/base"; rm -rf "$base_dir"
  git clone -q --shared --no-checkout "$PWD" "$base_dir" && git -C "$base_dir" checkout -q --detach "$sha" \
    && { git -C "$base_dir" show-ref -q --verify refs/heads/main || git -C "$base_dir" branch -q main origin/main 2>/dev/null; true; } \
    || { echo "no base clone; counts are not compared with the base"; rm -rf "$base_dir"; base_dir=""; }
else
  echo "no base ${2:-origin/main}; counts are not compared with the base"
fi

worst=0 i=0 lines=()
for row in "${rows[@]}"; do
  i=$((i + 1)) feature="${row%%$'\t'*}" cmd="${row#*$'\t'}"
  log="$dir/${feature// /-}.log" base_log="$dir/${feature// /-}.base.log" start=$SECONDS
  bash -c "$cmd" < /dev/null 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  args=("$status" "$log")
  if [[ -n "$base_dir" ]]; then
    (cd "$base_dir" && bash -c "$cmd" < /dev/null > "$base_log" 2>&1)
    args+=("$base_log")
  fi
  result="$(python3 -I "$here/results.py" "${args[@]}")"; code=$?
  (( code > 2 )) && { result="NOT VERIFIED: results.py exit $code"; code=1; }
  mark="✔"; (( code )) && mark="✘"
  echo "[$i/$total] $mark $feature ($((SECONDS - start))s) $result" | tee -a "$log"
  word="${result%%:*}" why="${result#*: }"
  lines+=("$feature: $word ($why)  cmd: $cmd  evidence: $log")
  # Worst wins: NOT VERIFIED (1) over BLOCKED (2) over VERIFIED (0).
  if (( code == 1 )) || { (( code == 2 )) && (( worst == 0 )); }; then worst=$code; fi
done
printf '\n'; printf '%s\n' "${lines[@]}"
overall=VERIFIED; (( worst == 1 )) && overall="NOT VERIFIED"; (( worst == 2 )) && overall=BLOCKED
echo "overall: $overall  evidence: $dir"
exit $worst
