#!/usr/bin/env python3
"""Checks that the repo follows trunk-based development (AGENTS.md).

A branch other than main may hold commits that main lacks for less than a day. Older, it is a
side branch that drifts, and its merge or restack redoes work. Local and origin branches count;
a branch already merged into main passes, since it drifts no further.

Usage: check_trunk.py [repo]   (default: this script's repo)
"""
import pathlib
import subprocess
import sys
import time

MAX_AGE = 24 * 3600
TRUNK = "main"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def main():
    repo = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
    refs = git(repo, "for-each-ref", "--format=%(refname:short) %(committerdate:unix)", "refs/heads", "refs/remotes/origin")
    now = time.time()
    bad = []
    for line in refs.splitlines():
        name, stamp = line.rsplit(" ", 1)
        if name in (TRUNK, f"origin/{TRUNK}", "origin/HEAD", "origin"):
            continue
        ahead = int(git(repo, "rev-list", "--count", f"{TRUNK}..{name}"))
        age = now - int(stamp)
        if ahead and age > MAX_AGE:
            bad.append(f"{name}: {ahead} commits not on {TRUNK}, last one {age / 3600:.0f} h ago; land it on {TRUNK} or delete it")
    for line in bad:
        print(line)
    if bad:
        return 1
    print("trunk ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
