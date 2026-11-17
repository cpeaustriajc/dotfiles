#!/usr/bin/env python3
"""Checks that each file a skill names exists, lies in that skill, and that copies match their source.

Usage: python3 -I scripts/check_skill_refs.py [root]

Checks Markdown under plugins/*/skills/*/ and .claude/skills/*/. A named path is a
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
    for pattern in ("plugins/*/skills/*/**/*.md", ".claude/skills/*/**/*.md"):
        yield from sorted(root.glob(pattern))


def skill_root(path, root=ROOT):
    rel = path.relative_to(root).parts
    return root.joinpath(*rel[:4] if rel[0] == "plugins" else rel[:3])


# Each skill works alone, so a file that several skills need is copied into each of them.
# The first path is the source; each copy must stay equal to it.
E = "plugins/engineering/skills/"
P = "plugins/planning/skills/"
COPIES = {
    E + "review-loop/references/tests.md": [E + "blast-radius/references/tests.md", E + "break-it/references/tests.md",
                                            E + "implement/references/tests.md"],
    E + "review-loop/scripts/tests_kept.py": [E + "create-pr/scripts/tests_kept.py"],
    E + "create-pr/references/stacking.md": [E + "implement/references/stacking.md"],
    E + "blast-radius/references/ai-tells.md": [E + "create-pr/references/ai-tells.md"],
    P + "shape/references/top-down.md": [P + s + "/references/top-down.md" for s in ("tickets", "triage", "vision")],
    P + "shape/references/tree-outline.md": [P + s + "/references/tree-outline.md" for s in ("tickets", "triage", "vision")],
    P + "shape/scripts/check_tree.py": [P + s + "/scripts/check_tree.py" for s in ("tickets", "triage", "vision")],
    P + "tickets/references/sizing.md": [P + "refine/references/sizing.md"],
    P + "vision/references/worth-it.md": [P + "scout/references/worth-it.md"],
    P + "grill/references/rounds.md": [P + "vision/references/rounds.md"],
}


def drifted(root, copies=COPIES):
    """Returns a line for each copy that is missing or differs from its source."""
    errors = []
    for src, dests in copies.items():
        for dest in dests:
            if not (root / dest).exists():
                errors.append(f"{dest}: missing copy of {src}")
            elif (root / dest).read_bytes() != (root / src).read_bytes():
                errors.append(f"{dest}: differs from {src}; edit the source, then copy it again")
    return errors


def crossing(path, text, root=ROOT):
    """Returns (line number, path) for each named path that points into another skill's folder."""
    own = skill_root(path, root)
    found = []
    for n, ref in named(text):
        target = (path.parent / ref).resolve()
        parts = target.relative_to(root).parts if target.is_relative_to(root) else ()
        if len(parts) > 3 and parts[0] == "plugins" and parts[2] == "skills" and root.joinpath(*parts[:4]) != own:
            found.append((n, ref))
    return found


def main(argv):
    root = pathlib.Path(argv[1]).resolve() if len(argv) > 1 else ROOT
    errors = []
    for path in markdown_files(root):
        roots = [path.parent, skill_root(path, root), root]
        text = path.read_text()
        for n, ref in dead(text, roots, lambda p: p.resolve().exists()):
            errors.append(f"{path.relative_to(root)}:{n}: names {ref}, which does not exist")
        for n, ref in crossing(path, text, root):
            errors.append(f"{path.relative_to(root)}:{n}: names {ref}, in another skill; copy it into this skill")
    if root == ROOT:
        errors += drifted(root)
    print("\n".join(errors) if errors else "skill refs ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
