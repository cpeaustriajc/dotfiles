---
paths:
  - "plugins/*/skills/*/README.md"
---

# README files for skills

Each skill folder has a `README.md`. A person reads it, not Claude: Claude
loads `SKILL.md`, never the README. `python3 -I scripts/check_readmes.py` checks
the structure, the sentence lengths and the banned words in Sentences.

## Reader

A developer who uses Claude Code but has never seen dotfiles. They give the README 30 seconds
to learn what the thing is, whether they need it, and how to turn it on.

## Write from the source

- Read the whole `SKILL.md` and its `references/` before you write. Every command, path, setting name and default in the README must
  exist in that source today. Never write a command you have not seen there or run.
- Do not copy the steps of `SKILL.md` into the README. Say what happens in terms the reader
  sees (files written, questions asked, actions blocked), then link to `SKILL.md` for the method.
- A value that changes often (a cap, a version, a count) has a single source of truth. Name the file.

## Structure

Line 1 is `# <folder name>`. Then one or two sentences: what it is and what it does for the
reader.

Then these `##` headings, in this order, with no other `##` headings:

| Section | What it answers |
|---|---|
| When to use it | the problem it solves, when not to use it, and which neighbour skill to use then |
| Example | you say X, Claude does Y, you get Z |
| Install | which plugin ships it and the install command |
| What it does | what it reads, writes, asks, blocks or changes |
| Limits | what it does not do |
| More | links to `SKILL.md`, `references/` |

Keep the README under 100 lines. Use `###` headings inside a section only when it is long.

## Sentences (ASD-STE100)

- A step in a numbered list: at most 20 words, one instruction, imperative ("Run", "Open").
- Any other sentence, list item or table cell: at most 25 words. A paragraph: at most 6
  sentences, about one topic.
- Address the reader as "you". Keep the articles ("the", "a").
- Define a dotfiles or Claude Code term at its first use, or link it.
- No abbreviations such as "e.g." or "i.e.". No filler ("simply", "just", "powerful",
  "seamless"), no hedging, no marketing tone, no emoji.
- Lead each heading, bullet and paragraph with the word that carries the information.

## Check

`plugins/engineering/skills/create-pr/README.md` and `plugins/knowledge/skills/hone/README.md` show the expected result.

Run `python3 -I scripts/check_readmes.py`. Then read the README as the reader above: can you say
in one sentence what it does, when you would use it, and how to turn it on?
