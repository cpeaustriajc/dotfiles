#!/usr/bin/env bash
# Re-runnable check of ghwiki.sh against a local bare repo (GHWIKI_REMOTE).
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
export XDG_CACHE_HOME=$tmp/cache GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
git init -q --bare "$tmp/wiki.git" && git clone -q "$tmp/wiki.git" "$tmp/seed" 2>/dev/null
echo hi > "$tmp/seed/Home.md"; git -C "$tmp/seed" add -A; git -C "$tmp/seed" commit -qm seed; git -C "$tmp/seed" push -q origin HEAD 2>/dev/null
export GHWIKI_REMOTE=$tmp/wiki.git
pass=0 fail=0
ok() { if [ "$2" = "$3" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL $1: got '$2', want '$3'"; fi; }
has() { case $2 in *$3*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo "FAIL $1: '$2' lacks '$3'" ;; esac; }

has help "$("$here/ghwiki.sh" --help)" "detect"
ok detect "$("$here/ghwiki.sh" detect o/r)" exists
dir=$("$here/ghwiki.sh" path o/r 2>/dev/null)
ok list "$("$here/ghwiki.sh" list o/r 2>/dev/null)" Home
echo x > "$dir/Decision-001-A.md"
"$here/ghwiki.sh" save o/r -m add >/dev/null 2>&1
has status "$("$here/ghwiki.sh" status o/r 2>/dev/null)" "ahead 1"
"$here/ghwiki.sh" push o/r -m add >/dev/null 2>&1
ok pushed "$(git -C "$tmp/wiki.git" log --format=%s -1)" add
"$here/ghwiki.sh" save o/r >/dev/null 2>&1; ok save-needs-message "$?" 2
"$here/ghwiki.sh" bogus >/dev/null 2>&1; ok unknown "$?" 2
echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
