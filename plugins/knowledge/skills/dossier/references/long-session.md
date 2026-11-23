# Long sessions

Setup writes three pieces that keep a long session on track after compaction. Each is committed,
so a cloud session reads it too. This file and the `compact_reinject` scripts stay out of the
project's copy of this skill.

## 1. Summary instructions

Copy `scripts/compact_focus.py` into the project's hooks folder. The settings block of piece 3
runs it before each compaction (`PreCompact` where the harness has one), and its output joins
the summarizer's instructions. Delete an older `# Compact instructions` section from the root
instruction file, because the harness does not apply it. A harness with no hook before
compaction: put the script's text in that section instead.

## 2. The rule

Write it as its own unscoped file in the harness's rules folder, so every session loads it. The
tracker is the one the project's instruction file names, else ask me.

```markdown
- Long session (a compaction, or more than one PR open): keep the open items, the open PRs and
  what was checked in one list in <tracker>, else an artifact; read it again after a
  compaction. In chat, mention an item only when it is new or changed; drop it once answered.
```

While the hook's trial runs (`TRIAL = True` in the script), the rule leaves out the hook's
"newest steer" step, so the two halves differ by that step alone. If the trial keeps the hook,
add the step to the rule.

## 3. The hook

Copy `scripts/compact_reinject.py` into the project's hooks folder and merge
`scripts/compact_reinject.settings.json` into the project's hook settings, creating the file when
missing, unless an entry already runs the same command. A harness with no hook after compaction:
skip it and say so. A session that loads no repository hooks still gets piece 2.

## Evidence

- In two losses after compaction, the summary held the fact and the next turn did not act on
  it, so the pieces point at the summary's newest steer instead of adding facts.
- The hook is a trial: it logs which half of the sessions got its text. Compare corrections
  after compaction per half before keeping it.
- A `# Compact instructions` section was applied in 0 of 354 compactions
  (`anthropics/claude-code#89797`) and in 0 of 3 tests on 2026-11-19. The hook before
  compaction reached the summary in 3 of 3, auto-compaction included.
- In a replay of a real session on 2026-11-19, the summary kept 2 of 10 of the agent's
  decisions without that hook and 3 with it. One run each, so the gain is unproven.
