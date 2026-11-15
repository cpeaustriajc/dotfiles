#!/usr/bin/env python3
"""Checks the text a model reads in each shipped skill: token cost, sentence length, filler, harness names.

Usage: python3 -I scripts/check_skills.py [--report]

Scans every Markdown file under plugins/*/skills/*/ except README.md (check_readmes.py owns those).
Tokens are characters / 4, the estimate `claude plugin details` reports. The every-turn cost (each
skill's name and description, together) has a hard limit; --report adds each skill's on-use cost.
.claude/rules/skills.md gives the sources. Sentence, filler and name checks skip the frontmatter.
"""
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_readmes import banned, words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_ALWAYS_ON = 2000  # tokens: every skill's name and description, loaded every turn, all together
TARGET_ALWAYS_ON = 1000
MAX_SKILL_TOKENS = 5000  # one SKILL.md: after compaction only its first 5,000 tokens are re-attached
MAX_SENTENCE = 50  # words between [.!?;] after joining wrapped lines; longest today: 49
# A skill runs on any harness and model (AGENTS.md: "A skill names no harness").
HARNESS = re.compile(r"\b(?:Claude|Anthropic|Codex|OpenAI|ChatGPT|GPT-\d\w*|Gemini|Copilot|Cursor|Windsurf|Kiro"
                     r"|Aider|Opus|Sonnet|Haiku|Fable)\b")
# Named exceptions: (path, harness name or the first words of a long sentence) -> why it stays.
EXCEPTIONS = {
    ("plugins/design/skills/ui-polish/references/quality-bar.md", "Cursor"): "a company in a list of product designs",
    ("plugins/design/skills/launch-video/references/voice.md", "OpenAI"): "who runs the Whisper server",
    ("plugins/knowledge/skills/dossier/references/publish.md", "Claude"): "the text to scrub before publishing",
    ("plugins/engineering/skills/blast-radius/references/ai-tells.md", "Substrate (base)"): "a list of words to avoid",
}


def files():
    """Every Markdown file the model may read; README.md is for people, evals/ for the eval runner."""
    for p in sorted(ROOT.glob("plugins/*/skills/*/**/*.md")):
        if p.name != "README.md" and p.is_file() and "evals" not in p.relative_to(ROOT).parts[4:]:
            yield p


def body(text):
    """The lines with a leading frontmatter block blanked, so line numbers stay true."""
    lines = text.splitlines()
    if lines and lines[0] == "---" and "---" in lines[1:]:
        end = lines.index("---", 1)
        lines = [""] * (end + 1) + lines[end + 1:]
    return lines


def tokens(text):
    return math.ceil(len(text) / 4)


def frontmatter(text):
    """The frontmatter lines, without the --- fences; none when there is no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return []
    return lines[1:lines.index("---", 1)]


def description(text):
    """The name and description from the frontmatter, joined as the skill listing shows them."""
    front = frontmatter(text)
    if not front:
        return ""
    found = {}
    for i, line in enumerate(front):
        m = re.match(r"(name|description):\s*(.*)", line)
        if not m:
            continue
        value = m.group(2).strip()
        if value in ("", ">", "|", ">-", "|-"):
            rest = []
            for x in front[i + 1:]:
                if not x[:1].isspace():
                    break
                rest.append(x.strip())
            value = " ".join(rest)
        found[m.group(1)] = value.strip("\"'")
    return f"{found.get('name', '')}: {found.get('description', '')}"


def costs():
    """Yields (skill folder, every-turn tokens, SKILL.md tokens, other files' tokens) for each skill.

    A typed-only skill (disable-model-invocation: true) costs 0 every turn: Claude Code's skills page
    says its "Description not in context". `claude plugin details` still counts it.
    """
    for skill in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        text = skill.read_text()
        typed = re.search(r"^disable-model-invocation:\s*true\s*$", "\n".join(frontmatter(text)), re.M)
        rest = sum(tokens(p.read_text()) for p in files() if p != skill and skill.parent in p.parents)
        yield skill.parent, 0 if typed else tokens(description(text)), tokens(text), rest


def units(lines):
    """Yields (line number, text) for each paragraph, list item and table cell, wrapped lines joined."""
    fenced, start, buf = False, 0, []

    def flush():
        if buf:
            yield start, " ".join(buf)
            buf.clear()

    for n, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            yield from flush()
            fenced = not fenced
            continue
        if fenced or not s or s.startswith("#"):
            yield from flush()
            continue
        if s.startswith("|"):
            yield from flush()
            if not re.fullmatch(r"[\s|:-]*", s):
                yield from ((n, cell) for cell in s.strip("|").split("|") if cell.strip())
            continue
        item = re.match(r"(?:[-*+]|\d+\.)\s+(.*)", s)
        if item or not buf:
            yield from flush()
            start = n
        buf.append(item.group(1) if item else s)
    yield from flush()


def sentences(text):
    """A semicolon ends a clause the same as a full stop: a list joined by semicolons is a list."""
    return [s for s in re.split(r"(?<=[.!?;])\s+", text.strip()) if s]


def excepted(rel, key):
    return any(r == rel and key.startswith(k) for r, k in EXCEPTIONS)


def check(path):
    rel = str(path.relative_to(ROOT))
    lines = body(path.read_text())
    errors = []
    if path.name == "SKILL.md" and tokens(path.read_text()) > MAX_SKILL_TOKENS:
        errors.append(f"{rel}: {tokens(path.read_text())} tokens, at most {MAX_SKILL_TOKENS}; "
                      "move detail to a file the step that needs it reads")
    for n, text in units(lines):
        for s in sentences(text.replace("**", "")):
            if words(s) > MAX_SENTENCE and not excepted(rel, s):
                errors.append(f"{rel}:{n}: {words(s)} words in one sentence, at most {MAX_SENTENCE}: {s[:60]}...")
    for n, match in banned(lines):
        errors.append(f"{rel}:{n}: filler \"{match}\" (see .claude/rules/skills.md)")
    fenced = False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in HARNESS.finditer(re.sub(r"`[^`]*`", " ", line)):
            if (rel, m.group()) not in EXCEPTIONS:
                errors.append(f"{rel}:{n}: names \"{m.group()}\"; a skill names no harness or model vendor")
    return errors


def main(argv=()):
    errors = [e for p in files() for e in check(p)]
    rows = list(costs())
    always = sum(r[1] for r in rows)
    if always > MAX_ALWAYS_ON:
        errors.append(f"every-turn cost: {always} tokens of names and descriptions, at most {MAX_ALWAYS_ON}")
    if "--report" in argv:
        print("skill\tevery turn\tSKILL.md\tother files")
        for d, a, s, r in rows:
            print(f"{d.relative_to(ROOT)}\t{a}\t{s}\t{r}")
        print(f"total\t{always}\t{sum(r[2] for r in rows)}\t{sum(r[3] for r in rows)}")
    print("\n".join(errors) if errors else
          f"skills ok: every turn {always} tokens, limit {MAX_ALWAYS_ON}, target {TARGET_ALWAYS_ON}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
