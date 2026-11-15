#!/usr/bin/env python3
"""Runs a project's recent history through guard_tests.py's rules, so Setup can pick a mode.

Usage: python3 -I replay.py [--commits 200] [--config guard_tests.json]

Prints one JSON line: how many guarded file changes (a test or runner file modified or deleted) each
rule set would have asked about.
  commits  commits read (merges skipped)
  changes  guarded file changes seen
  full     changes the full rules would ask about
  rigs     changes the rig rules (the content rules only) would ask about
  capped   true when it stopped at CAP changes
Pick full when it would ask about few of the changes, rigs when full would ask about many, off only
when even the rig rules would ask about most. The replay reads commits, which are coarser than an
agent's edits. extra_test_dirs, extra_test_names and shared_files come from guard_tests.json beside
this script, or from --config; the mode in it is ignored.

exit 0  the counts; exit 2  {"error": ...}: not a git repository, or git failed
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I leaves the script's folder off sys.path
sys.dont_write_bytecode = True
import guard_tests as gt  # noqa: E402

COMMITS = 200
CAP = 300


def git(root, *args):
    r = subprocess.run(["git", *args], cwd=root, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def replay(root, commits=COMMITS, cfg=gt.DEFAULT):
    out = {"commits": 0, "changes": 0, "full": 0, "rigs": 0, "capped": False}
    rc, log, err = git(root, "log", "--no-merges", f"-n{commits}", "--no-renames", "--name-status", "-z", "--format=%x01%H %P")
    if rc:
        if re.search(r"does not have any commits yet", err):
            return out
        raise RuntimeError(f"git log exited {rc}: {err.strip()}")

    def show(spec):
        rc, text, _ = git(root, "show", spec)
        return text if rc == 0 else None

    for record in log.split("\x01")[1:]:
        header, *files = record.split("\0")
        ids = header.strip().split(" ")
        out["commits"] += 1
        if len(ids) < 2 or not ids[1]:
            continue
        sha = ids[0]
        for i in range(0, len(files) - 1, 2):
            status, rel = files[i].strip(), files[i + 1]
            kind = cfg.kind_of(rel)
            if status not in ("M", "D") or kind not in ("test", "config"):
                continue
            if out["changes"] == CAP:
                out["capped"] = True
                return out
            head = show(f"{sha}^:{rel}")
            text = "" if status == "D" else show(f"{sha}:{rel}")
            if head is None or text is None:
                continue
            out["changes"] += 1
            if gt.findings(kind, rel, head, text, cfg=cfg):
                out["full"] += 1
            if gt.findings(kind, rel, head, text, True, cfg=cfg):
                out["rigs"] += 1
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--commits", type=int, default=COMMITS, help="commits to read (default %(default)s)")
    ap.add_argument("--config", default=os.path.join(HERE, "guard_tests.json"), help="guard_tests.json to take the extra names from")
    args = ap.parse_args(argv)
    try:
        rc, top, err = git(".", "rev-parse", "--show-toplevel")
        if rc:
            raise RuntimeError("not a git repository")
        print(json.dumps(replay(top.strip(), max(args.commits, 1), gt.load_config(args.config))))
    except (RuntimeError, OSError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
