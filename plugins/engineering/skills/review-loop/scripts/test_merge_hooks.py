#!/usr/bin/env python3
"""Tests merge_hooks.py: both hook blocks land once, other keys and entries stay, bad input fails.

Run: python3 -I test_merge_hooks.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from merge_hooks import merge  # noqa: E402

SCRIPT = os.path.join(HERE, "merge_hooks.py")
GUARD = os.path.join(HERE, "guard_tests.settings.json")
GATE = os.path.join(HERE, "..", "..", "implement", "scripts", "stop_gate.settings.json")
passed = failed = 0


def case(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got!r}, want {want!r}")


def run(*args):
    r = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def entry(cmd, matcher=None):
    e = {"hooks": [{"type": "command", "command": cmd}]}
    if matcher:
        e["matcher"] = matcher
    return e


block = {"hooks": {"Stop": [entry("a")], "PreToolUse": [entry("a", "Bash")]}}
case("an empty file gets every entry", merge({}, block)[1], 2)
case("a second merge adds nothing", merge(merge({}, block)[0], block)[1], 0)
mine = {"model": "x", "hooks": {"Stop": [entry("mine")]}}
out, n = merge(mine, block)
case("other keys stay", out["model"], "x")
case("an entry already there stays first", [e["hooks"][0]["command"] for e in out["hooks"]["Stop"]], ["mine", "a"])

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, ".claude", "settings.json")
    case("the CLI adds the guard to a missing file", run(path, GUARD), (0, "added 4"))
    case("the CLI adds the gate beside it", run(path, GATE), (0, "added 3"))
    case("a second run is unchanged", (run(path, GUARD), run(path, GATE)), ((0, "unchanged"), (0, "unchanged")))
    with open(path, encoding="utf-8") as f:
        hooks = json.load(f)["hooks"]
    case("Stop runs both hooks once", sorted(c.rsplit("/", 1)[1] for c in __import__("merge_hooks").commands(hooks["Stop"])),
         ["guard_tests.py", "stop_gate.py"])
    bad = os.path.join(tmp, "bad.json")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("[]")
    case("a JSON list is refused", run(bad, GUARD)[0], 1)

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
