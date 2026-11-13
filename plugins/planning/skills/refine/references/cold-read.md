# Cold read

Read this before you brief the cold reader. The steps are in `SKILL.md`.

## The brief

Give the reader the draft, the sources and the personas below. Keep the read blind: leave out
your reasoning, the gap list and the earlier drafts. A reader that knows why a line exists skips
past it.

The reader takes each persona in turn:

- **User**: what does the user see in each state, including the stale and chained ones?
- **QA**: can each check pass or fail today, on its environment, with its fixture?
- **Builder**: is the ticket self-contained, so that one agent can finish and prove it?
- **Red team**: what does a replayed, raced or forged request do?

## Findings

The reader writes them beside the draft, one per line:

```
<ticket> · blocker | slip | decision · <what a reader trips on> · <the source that shows it>
```

- **blocker**: a behaviour that no line covers, a check nobody can run, or two tickets that
  disagree.
- **slip**: a wrong count or name, or a stale cross-reference. The reader fixes it in the draft.
- **decision**: two ways that both work. The reader names both and does not pick one.

The reader ends by marking each fix from the last round as fixed, partly fixed or missing.

## Seen in the session this came from

| Draft | Reader | Found |
|---|---|---|
| 10 | Opus, cold read | 25 problems, 9 of them blockers |
| 11 | Opus, cold read | 23 problems; 19 earlier fixes confirmed, 6 partly fixed |
| 12 | Sonnet, check and tidy | 4 slips, 1 decision |
