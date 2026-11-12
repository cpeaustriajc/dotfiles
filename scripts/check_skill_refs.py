#!/usr/bin/env python3
"""Checks that each file a skill or mod README names exists.

Usage: python3 -I scripts/check_skill_refs.py [root]

Checks Markdown under plugins/*/skills/*/, .claude/skills/*/ and mods/*/README.md. A named path is a
relative Markdown link target, or a backticked path with a known extension whose first part is one
of OWN_DIRS or "..". A path passes if it exists next to the file, in the skill's root, or in the repo.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OWN_DIRS = {"references", "scripts", "library", "assets", "agents", ".."}
EXTENSIONS = r"(?:md|py|sh|mjs|ts|json|ya?ml)"
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TICKS = re.compile(r"`([^`\n]+)`")
PATH = re.compile(rf"[\w.-]+(?:/[\w.-]+)+\.{EXTENSIONS}(?:#[\w-]*)?")
SKIP = re.compile(r"[<>*{}$~]|^/|^[a-z][a-z0-9+.-]*:|^#")


def named(text):
    """Yields (line number, path) for each file a Markdown text names, outside code fences."""
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in LINK.findall(line):
            if not SKIP.search(target):
                yield n, target.split("#")[0]
        for token in TICKS.findall(line):
            token = token.removeprefix("./")
            if PATH.fullmatch(token) and not SKIP.search(token) and token.split("/")[0] in OWN_DIRS:
                yield n, token.split("#")[0]


def dead(text, roots, exists):
    """Returns (line number, path) for each named path that exists under none of roots."""
    return [(n, p) for n, p in named(text) if p and not any(exists(r / p) for r in roots)]


def markdown_files(root=ROOT):
    for pattern in ("plugins/*/skills/*/**/*.md", ".claude/skills/*/**/*.md", "mods/*/README.md"):
        yield from sorted(root.glob(pattern))


def skill_root(path, root=ROOT):
    rel = path.relative_to(root).parts
    if rel[0] == "mods":
        return root / "mods" / rel[1]
    return root.joinpath(*rel[:4] if rel[0] == "plugins" else rel[:3])


def main(argv):
    root = pathlib.Path(argv[1]).resolve() if len(argv) > 1 else ROOT
    errors = []
    for path in markdown_files(root):
        roots = [path.parent, skill_root(path, root), root]
        for n, ref in dead(path.read_text(), roots, lambda p: p.resolve().exists()):
            errors.append(f"{path.relative_to(root)}:{n}: names {ref}, which does not exist")
    print("\n".join(errors) if errors else "skill refs ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
