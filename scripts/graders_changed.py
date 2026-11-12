#!/usr/bin/env python3
"""Fails when a change touches a grader: the files that judge a pull request.

Usage: <changed paths, one per line> | python3 -I scripts/graders_changed.py

The workflow .github/workflows/graders.yml runs this from the base branch on the PR's file list,
so the PR cannot edit it. When it passes, the checks job ran the base's graders on the PR's content.
When it fails, the owner reads the grader diff and merges past the check; an agent cannot.
"""
import sys

GRADERS = (
    ".github/",
    ".gitattributes",
    "scripts/",
    ".claude/skills/verify/",
    ".claude/skills/run-dotfiles/",
    "plugins/engineering/skills/review-loop/scripts/",
    "tests/claude-owned/",
)


def graders(paths):
    return [p for p in paths if p == ".gitattributes" or any(p.startswith(g) for g in GRADERS if g.endswith("/"))]


def main():
    paths = [p.strip() for p in sys.stdin if p.strip()]
    hits = graders(paths)
    for p in hits:
        print(f"{p}: changes a grader; the owner reviews the diff and merges past this check")
    if not hits:
        print(f"graders unchanged: {len(paths)} files checked")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
