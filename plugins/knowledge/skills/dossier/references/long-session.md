# Long sessions

Setup step of SKILL.md. Three pieces keep a long session on track after its context is
compacted. Each goes where a cloud session still reads it: committed, at the repository root.

## 1. Summary instructions

Add this section to the root instruction file, under the heading the harness reads for
compaction (`# Compact instructions` where it has one). Replace an older copy of the section.

```markdown
# Compact instructions

Quote the user's newest request and every correction or decision in their own words, newest
first. Keep the open PRs, branches, running sessions and subagents with their ids and state,
and where the open-items list is kept.
```

## 2. The rule

Write it as its own file in the folder where the harness loads a repository's rules, unscoped,
so it loads in every session. Name the project's tracker, from the Backend section.

```markdown
- Long session (a compaction, or more than one PR open): keep the open items, the open PRs and
  what was checked in one list in <tracker>, else an artifact. After a compaction, act on the
  user's newest request and steer as the summary quotes them, not on the older plan; then read
  that list again. Example: the summary quoted "look up the checker first", and the next turn
  went back to timing the old script. In chat, mention an item only when it is new or changed;
  drop it once answered.
```

## 3. The hook

Copy `scripts/compact_reinject.py` into the project's hooks folder and merge
`scripts/compact_reinject.settings.json` into the project's hook settings: add the entry only
when no entry runs the same command. A harness with no hook after compaction: skip it and say
so. A session that loads no repository hooks still gets pieces 1 and 2.

## Evidence

- In two losses after compaction, the summary already held the fact, and the next turn did not
  act on it. So the pieces point at the summary's newest steer instead of adding facts.
- The hook is a trial: it logs which half of the sessions got its text. Compare corrections
  after compaction per half before keeping it.
