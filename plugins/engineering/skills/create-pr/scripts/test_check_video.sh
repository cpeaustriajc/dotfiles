#!/usr/bin/env bash
# Re-runnable check of check-video.sh on generated clips. Needs ffmpeg and ffprobe.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
passed=0; failed=0

make() { ffmpeg -v error -y -f lavfi -i "$1" -t 6 -pix_fmt yuv420p "$tmp/$2.mp4"; }
make "testsrc=size=320x240:rate=25" moving
make "color=c=blue:size=320x240:rate=25" still
# 1 s of motion, then 5 s frozen on the last frame.
make "testsrc=size=320x240:rate=25,trim=0:1,tpad=stop_mode=clone:stop_duration=5" mostly_still

case_() { # name file want_exit want_text
  out="$(bash "$here/check-video.sh" "$tmp/$2.mp4" 2>&1)"; st=$?
  if [[ $st -eq $3 && "$out" == *"$4"* ]]; then passed=$((passed + 1)); echo "ok   $1"
  else failed=$((failed + 1)); echo "FAIL $1: exit $st"; echo "$out" | sed 's/^/     /'; fi
}

case_ "a moving clip passes" moving 0 "PASS"
case_ "a still clip fails" still 1 "FAIL still"
case_ "a clip frozen for most of its length fails" mostly_still 1 "FAIL still"

echo "$passed passed, $failed failed"
exit $(( failed > 0 ))
