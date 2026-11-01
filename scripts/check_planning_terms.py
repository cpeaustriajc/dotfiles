#!/usr/bin/env python3
"""Checks that the planning skills use no tracker's own section names.

"Done When" is Linear's habit, not a neutral term. A skill that writes it pushes one tracker's
practice onto every project; the project's own template names its sections, and the skills say
"checks". This scans the planning plugin and the evals that drive it.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNED = re.compile(r"done[ _-]when", re.I)
SCOPE = ["plugins/planning", "evals/routing", "evals/behaviour"]


def main():
    bad = []
    for top in SCOPE:
        for path in sorted((ROOT / top).rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".py", ".json", ".sh", ".yaml"}:
                continue
            for n, line in enumerate(path.read_text().splitlines(), 1):
                if BANNED.search(line):
                    bad.append(f"{path.relative_to(ROOT)}:{n}: \"Done When\" is a tracker term; say \"checks\"")
    for line in bad:
        print(line)
    if bad:
        return 1
    print("planning terms ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
