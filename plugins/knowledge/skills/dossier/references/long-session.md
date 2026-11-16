# Long sessions

Setup writes three pieces that keep a long session on track after compaction. Each is committed,
so a cloud session reads it too. This file and the `compact_reinject` scripts stay out of the
project's copy of this skill.

## 1. Summary instructions

Add this section to the root instruction file, creating it when missing, under the heading the
harness reads for compaction (`# Compact instructions` where it has one). It replaces an older
copy.

```markdown
# Compact instructions

Quote the user's newest request and every correction or decision in their own words, newest
first. Keep the open PRs, branches, running sessions and subagents with their ids and state,
and where the open-items list is kept.
```

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
skip it and say so. A session that loads no repository hooks still gets pieces 1 and 2.

## Evidence

- In two losses after compaction, the summary held the fact and the next turn did not act on
  it, so the pieces point at the summary's newest steer instead of adding facts.
- The hook is a trial: it logs which half of the sessions got its text. Compare corrections
  after compaction per half before keeping it.
