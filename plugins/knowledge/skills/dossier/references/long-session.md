# Long sessions

Setup step of SKILL.md. Three pieces keep a long session on track after its context is
compacted. Each is committed in the repository, where a cloud session still reads it. They stay
out of the project's copy of this skill, with this file and the `compact_reinject` scripts.

## 1. Summary instructions

Add this section to the root instruction file the harness reads, creating it when missing,
under the heading the harness reads for compaction (`# Compact instructions` where it has one).
Replace an older copy of the section.

```markdown
# Compact instructions

Quote the user's newest request and every correction or decision in their own words, newest
first. Keep the open PRs, branches, running sessions and subagents with their ids and state,
and where the open-items list is kept.
```

## 2. The rule

Write it as its own file in the folder where the harness loads a repository's rules, unscoped,
so it loads in every session. Name the issue tracker the project's instruction file names, else
ask me.

```markdown
- Long session (a compaction, or more than one PR open): keep the open items, the open PRs and
  what was checked in one list in <tracker>, else an artifact; read it again after a
  compaction. In chat, mention an item only when it is new or changed; drop it once answered.
```

While the hook's trial runs (`TRIAL = True` in the script), the rule leaves out the hook's "newest steer" step, so the two
halves differ by that step alone. If the trial keeps the hook, add the step to the rule too.

## 3. The hook

Copy `scripts/compact_reinject.py` into the project's hooks folder and merge
`scripts/compact_reinject.settings.json` into the project's hook settings, creating the file
when missing: add the entry only when no entry runs the same command. A harness with no hook after compaction: skip it and say
so. A session that loads no repository hooks still gets pieces 1 and 2.

## Evidence

- In two losses after compaction, the summary already held the fact, and the next turn did not
  act on it. So the pieces point at the summary's newest steer instead of adding facts.
- The hook is a trial: it logs which half of the sessions got its text. Compare corrections
  after compaction per half before keeping it.
