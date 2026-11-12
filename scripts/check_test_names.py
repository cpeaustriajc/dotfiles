#!/usr/bin/env python3
"""Checks that test-guard and tests_kept.py agree on which paths are test files.

Usage: python3 -I scripts/check_test_names.py [root]
Exits 1 with one path:line: cause per difference, or when a definition is missing.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUARD = "mods/test-guard/hooks/check.ts"
KEPT = "plugins/engineering/skills/review-loop/scripts/tests_kept.py"


def block(text, start, end):
    """Returns (line number, text) from the line with `start` through the first `end` after it, or None."""
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i)
    return (text.count("\n", 0, i) + 1, text[i:j]) if j >= 0 else None


def guard(text):
    names = block(text, "const TEST_NAME = [", "]\n")
    dirs = block(text, "const TEST_DIR = new Set([", "])")
    if not names or not dirs:
        return None
    literals = re.findall(r"/(.+?)/(?:,\s*|$)", names[1].split("[", 1)[1].strip())
    patterns = [p.replace("\\/", "/") for p in literals]
    return (names[0], patterns), (dirs[0], set(re.findall(r"'([^']*)'", dirs[1])))


def kept(text):
    names = block(text, "TEST_NAME = [", ")]")
    dirs = block(text, "TEST_DIR = {", "}")
    if not names or not dirs:
        return None
    return (names[0], re.findall(r'r"((?:\\.|[^"\\])*)"', names[1])), (dirs[0], set(re.findall(r'"([^"]*)"', dirs[1])))


def compare(guard_text, kept_text, guard_path=GUARD, kept_path=KEPT):
    """Returns the error lines; empty when the two agree."""
    g, k = guard(guard_text), kept(kept_text)
    errors = [f"{path}:1: no TEST_NAME and TEST_DIR definition found" for path, d in ((guard_path, g), (kept_path, k)) if d is None]
    if errors:
        return errors
    (gn, gp), (gd, gdirs) = g
    (kn, kp), (kd, kdirs) = k
    for p in gp:
        if p not in kp:
            errors.append(f"{kept_path}:{kn}: name pattern missing, {guard_path} has {p}")
    for p in kp:
        if p not in gp:
            errors.append(f"{guard_path}:{gn}: name pattern missing, {kept_path} has {p}")
    if gp != kp and sorted(gp) == sorted(kp):
        errors.append(f"{kept_path}:{kn}: name patterns are in a different order than {guard_path}")
    for d in sorted(gdirs - kdirs):
        errors.append(f"{kept_path}:{kd}: folder missing, {guard_path} has {d}")
    for d in sorted(kdirs - gdirs):
        errors.append(f"{guard_path}:{gd}: folder missing, {kept_path} has {d}")
    return errors


def main(argv):
    root = pathlib.Path(argv[1]) if len(argv) > 1 else ROOT
    errors = compare((root / GUARD).read_text(), (root / KEPT).read_text())
    print("\n".join(errors) if errors else "test names ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
