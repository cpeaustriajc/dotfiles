#!/usr/bin/env bash
# Tests drive.sh on a throwaway repo: a pass needs a result line, zero failures and the base's count.
set -uo pipefail
drive="$(cd "$(dirname "$0")" && pwd)/drive.sh"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
git init -q -b main "$tmp/repo" && cd "$tmp/repo" || exit 1
printf 'printf " 3 pass\\n 0 fail\\n"\n' > t.sh
git add t.sh && git commit -qm base
git update-ref refs/remotes/origin/main HEAD
pass=0 fail=0

# expect <name> <want exit> <want text> <rows>
expect() {
  local out code; out="$(printf '%s\n' "$4" | bash "$drive" "$tmp/logs" 2>&1)"; code=$?
  if [[ $code == "$2" && "$out" == *"$3"* ]]; then pass=$((pass + 1)); echo "ok   $1"
  else fail=$((fail + 1)); echo "FAIL $1: exit $code, want $2 and '$3' in:"; echo "$out" | tail -4; fi
}

expect "a result line with no failures is VERIFIED" 0 "a: VERIFIED (3 passed, 0 failed (base ran 3))" $'a\tbash t.sh'
expect "exit 0 with no result line is NOT VERIFIED" 1 "a: NOT VERIFIED (exit 0 but no runner result line" $'a\texit 0'
expect "|| true over a failure is NOT VERIFIED" 1 "NOT VERIFIED (exit 0 but 1 failed" $'a\tprintf " 2 pass\\n 1 fail\\n"; false || true'
expect "zero tests is NOT VERIFIED" 1 "NOT VERIFIED (0 passed" $'a\tprintf " 0 pass\\n 0 fail\\n"'
expect "exit 2 is BLOCKED" 2 "a: BLOCKED (BLOCKED: no token)" $'a\techo "BLOCKED: no token"; exit 2'
expect "one bad feature makes the overall NOT VERIFIED" 1 "overall: NOT VERIFIED" $'a\tbash t.sh\nb\texit 0'
expect "BLOCKED and VERIFIED is BLOCKED overall" 2 "overall: BLOCKED" $'a\tbash t.sh\nb\texit 2'
printf 'printf " 2 pass\\n 0 fail\\n"\n' > t.sh
expect "fewer than the base ran is NOT VERIFIED" 1 "2 passed, but the same command ran 3 at the base" $'a\tbash t.sh'
git commit -qam fewer
expect "a committed drop is still below the base" 1 "ran 3 at the base" $'a\tbash t.sh'

echo "$pass passed, $fail failed"
(( fail == 0 ))
