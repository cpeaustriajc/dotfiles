# Evidence rules and the answer

Steps 4 and 5 of `SKILL.md`.

## Tiers (step 4)

Label every claim with one tier:

| Tier | Needs |
|---|---|
| Direct | an author's own words: commit message, PR body, review comment, ticket, doc |
| Supported | two or more sources that agree, each cited, none stating it outright |
| Inferred | a reasoned step from cited evidence; write "appears to" or "is consistent with" |
| Speculative | a plausible reading with no evidence; say so |
| Unknown | searched and not found; say where you searched |

- "Because", "was designed to", "fixes" and "the team decided" go only beside a Direct or
  Supported citation.
- Mechanics are not motivation: a diff from `50` to `100` shows the change, not the reason.
- Code style and behaviour show no intent: a neat pattern can be copy and paste.
- Trace back to the commit that added the line, and follow revert-then-reapply chains; the
  latest commit is not the whole story.
- Evidence about a neighbour (another flag, another endpoint) does not answer for the target.
- If sources disagree, show both, side by side, with citations. Do not pick the tidy one.
- Before you call evidence strong, ask: would I see this if my reading were wrong?
- Check each citation you present (hash, PR number, line) exists.

## Answer (step 5)

In the chat:

1. **Question and target**: one line each, with `file:line`.
2. **Found**: Direct and Supported claims, each with its citation.
3. **Inferred**: hedged, each with the evidence it rests on.
4. **Candidates**: each reading, my guess included, with evidence for and against.
5. **Unknown**: what no source answers, and who could (the commit author, the PR reviewer).
6. **Sources**: one line each: searched (the queries), empty, or unavailable. No access is a gap,
   not a "no".
7. **Preserve, Change, Avoid, Risk**: four lines for a change to this code. If I asked whether
   to delete it, Risk says what returns when it goes.
