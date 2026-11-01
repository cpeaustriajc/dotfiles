#!/usr/bin/env python3
"""Checks that each typed skill stays typed in Codex too.

Claude Code reads `disable-model-invocation: true` from SKILL.md. Codex ignores it and reads
`policy.allow_implicit_invocation: false` from agents/openai.yaml
(https://learn.chatgpt.com/docs/build-skills). Without the second file, a skill linked into
~/.agents/skills by scripts/link-skills.sh starts on its own in Codex.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPED = re.compile(r"^disable-model-invocation:\s*true\s*$", re.M)
POLICY = re.compile(r"^policy:\s*\n\s+allow_implicit_invocation:\s*false\s*$", re.M)


def frontmatter(text):
    parts = text.split("---", 2)
    return parts[1] if text.startswith("---") and len(parts) == 3 else ""


def main():
    bad = []
    for skill_md in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        skill = skill_md.parent
        rel = skill.relative_to(ROOT)
        typed = bool(TYPED.search(frontmatter(skill_md.read_text())))
        yaml = skill / "agents" / "openai.yaml"
        blocked = yaml.is_file() and bool(POLICY.search(yaml.read_text()))
        if typed and not blocked:
            bad.append(f"{rel}: typed in SKILL.md, but agents/openai.yaml lacks allow_implicit_invocation: false")
        if blocked and not typed:
            bad.append(f"{rel}: agents/openai.yaml blocks implicit use, but SKILL.md is not typed")
    for line in bad:
        print(line)
    if bad:
        return 1
    print("typed skills ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
