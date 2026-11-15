---
paths:
  - "plugins/*/skills/**"
---

# Skill text

The model reads every Markdown file in a skill folder except `README.md` (`wiki.md` covers the
README). Write it short, plain and vendor neutral. A skill costs nothing until it runs: only its
name and description load every turn; `SKILL.md` loads when the skill runs; any other file loads
only at the step that reads it. Keep project detail in the project copy that Setup writes.

`python3 -I scripts/check_skills.py` fails on the limits below; `--report` prints each skill's
cost. A token is 4 characters, the estimate `claude plugin details` prints.

| Check | Limit | Source |
|---|---|---|
| Every skill's name and description, all together; a skill with `disable-model-invocation: true` counts 0 | 2,000 tokens; target 1,000 | Claude Code's skills page: the listing of names and descriptions loads every turn, its budget "scales at 1% of the model's context window", and it is shared with every other installed skill; on overflow, descriptions are dropped. For a typed-only skill: "Description not in context". 2,000 tokens is 1% of 200K. |
| One `SKILL.md` | 5,000 tokens | Claude Code docs: after compaction a skill keeps its first 5,000 tokens. |
| Words in one sentence, wrapped lines joined, `;` ends a sentence | 50 | Today's longest is 49. A hypothesis: no source sets one for model-read text. |
| Filler: the `check_readmes.py` list (`simply`, `just`, `e.g.`, emoji) | none | `wiki.md`. A hypothesis for model-read text. |
| Harness or model vendor names outside code | none | `AGENTS.md`: a skill names no harness. |

Raise a limit only with a reason in the PR. A justified name or sentence goes in `EXCEPTIONS` in
the script, with why it stays.

## What the check can't measure

- Whether a paragraph earns its tokens, or tells the model what it already knows.
- Whether a step reads a file only when it needs it, rather than up front.
- One term per idea throughout the skill.
- Over-compression: dropped articles, arrows and fragments pass the counts.
- Code-host and tracker names (GitHub, Linear, Jira) in the text.

Read the skill as a model that has never seen this repo. Then run `/doctor prompt-audit <path>`.
