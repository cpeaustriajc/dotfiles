#!/usr/bin/env python3
"""Checks that no skill, mod or eval uses a tracker's own section name.

"Done When" is Linear's habit, not a neutral term. A skill that writes it pushes one tracker's
practice onto every project; the project's own template names its sections, and the skills say
"checks" or "end state". This scans the tracked files under plugins/, mods/ and evals/. Prose such
as "should only be done when lowering it" passes: the check matches a capital "Done", or the
words joined by "-" or "_".
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNED = re.compile(r"\bDone[ _-][Ww]hen\b|\bdone[_-]when\b")
SCOPE = ["plugins", "mods", "evals"]


def main():
    files = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", *SCOPE],
                           check=True, capture_output=True, text=True).stdout.splitlines()
    bad = []
    for rel in files:
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if BANNED.search(line):
                bad.append(f"{rel}:{n}: \"Done When\" is a tracker term; say \"checks\" or \"end state\"")
    for line in bad:
        print(line)
    if bad:
        return 1
    print("tracker terms ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
