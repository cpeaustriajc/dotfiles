# Cold read

Read this before you brief the cold reader. The steps are in `SKILL.md`.

## The brief

The first read is blind and full: give the reader the draft, the sources and the personas below,
and leave out your reasoning and the gap list. A reader that knows why a line exists skips past it.

Each later read is a re-check: give the last round's findings and the lines the fixes changed.
The reader checks those, not the whole draft. After a split, the re-check reads the new items in
full, with what is exposed between one item and the next.

The reader takes each persona in turn:

- **User**: what does the user see in each state, including the stale and chained ones?
- **QA**: can each check pass or fail today, on its environment, with its fixture?
- **Builder**: is the ticket self-contained and within `../../tickets/references/sizing.md`, so
  that one agent can finish and prove it in one session?
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

A re-check marks each fix as fixed, partly fixed or missing; the last two count as blockers.

Failure: blind full reads of every draft found 17 to 25 problems a round for nine drafts, most
of them new wording, so the loop never reached a fixed point.

Failure (one run, 2026-11-14): seven tickets of 8,000 to 41,000 characters converged after 17
drafts, then failed the `tickets` size limits. A split late in the loop opened 11 blockers, and
the re-slice into 41 items needed a second blind read, which found 12 more.
