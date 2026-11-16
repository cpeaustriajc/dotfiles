#!/usr/bin/env python3
"""Tests compact_reinject.py by piping hook input into the script as a subprocess.

Run: python3 -I test_compact_reinject.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "compact_reinject.py")
passed = failed = 0
tmp = tempfile.mkdtemp()
LOG = os.path.join(tmp, "trial.log")


def report(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {detail}")


def hook(session_id, project, raw=None):
    env = dict(os.environ, COMPACT_TRIAL_LOG=LOG, CLAUDE_PROJECT_DIR=project)
    stdin = raw if raw is not None else json.dumps(
        {"session_id": session_id, "cwd": project, "hook_event_name": "SessionStart", "source": "compact"})
    p = subprocess.run([sys.executable, "-I", SCRIPT], input=stdin, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout.strip()


def context(out):
    try:
        return json.loads(out)["hookSpecificOutput"]["additionalContext"]
    except (ValueError, KeyError, TypeError):
        return None


repo = os.path.join(tmp, "repo")
os.makedirs(os.path.join(repo, ".claude", "work", "x"))
os.makedirs(os.path.join(repo, "node_modules", "pkg"))
open(os.path.join(repo, ".claude", "work", "x", "CHECKPOINT.md"), "w").close()
open(os.path.join(repo, "node_modules", "pkg", "PROGRESS.md"), "w").close()
bare = os.path.join(tmp, "bare")
os.makedirs(bare)

code, out = hook("022bf50b-0000-0000-0000-000000000000", bare)
text = context(out)
report("even id gets the text", code == 0 and text and "newest request" in text, out)
report("no checkpoint, no step 3", text and "Re-read:" not in text, out)

code, out = hook("03c808d2-0000-0000-0000-000000000001", bare)
report("odd id is the control", code == 0 and out == "", out)

code, out = hook("aa-c", repo)
text = context(out) or ""
report("names the checkpoint file", "CHECKPOINT.md" in text, out)
report("skips node_modules", "node_modules" not in text, out)

code, out = hook("", bare)
report("missing session id is silent", code == 0 and out == "", out)

code, out = hook("x", bare, raw="not json")
report("bad input is silent", code == 0 and out == "", out)

lines = open(LOG, encoding="utf-8").read().splitlines() if os.path.exists(LOG) else []
arms = {line.split("\t")[2] for line in lines}
report("logs one line per session with both arms", len(lines) == 3 and arms == {"reinject", "control"}, lines)

shutil.rmtree(tmp, ignore_errors=True)
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
