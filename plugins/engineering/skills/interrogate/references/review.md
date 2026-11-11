# Reviewers and judging

Steps 2 and 3 of `SKILL.md`.

## Reviewers (step 2)

Each reviewer sees a different slice of the bundle; diversity comes from the slice, not from
personas.

- **Full**: the whole bundle, on the session's model.
- **Blind**: the harness's built-in code review on the diff target, when the harness has one. It
  sees no description or spec, so it judges what the code does and catches what the description
  explains away. With no built-in, use a subagent on a cheaper model, with the diff and the
  changed files.
- **Spec**: only when a spec or issue exists. It gets the spec and the diff with no description,
  so it checks the code against what was asked, not what the author says was done.

Every subagent reviewer gets this prompt unchanged. A built-in review keeps its own:

> Review this change for real defects only: wrong behaviour, regressions, broken edge cases,
> security holes, data loss, divergence from the spec. No style, naming or "consider adding"
> notes. For each finding give: file:line, a one-line defect, a concrete failure scenario
> (input or state → wrong result), your confidence (high, medium or low), and the highest proof
> level that is true:
>
> - stated: claimed, with no location.
> - pointed at the line: file:line given.
> - walked through: the call path traced by hand, with the inputs that trigger it. Give the path.
> - run: a command, test or repro executed. Give the command and its output.
>
> If you find nothing real, say "no findings".

## Judge (step 3)

Merge duplicates and note which reviewers raised each. Verify each finding against the code
yourself: a reviewer can be confidently wrong. Your check sets the final proof level: raise it
when you trace the path or run a repro, lower it when the reviewer's path or output does not
hold.

- **Act on**: real, in scope, and walked through or run. Example: a null deref at cart.ts:42
  whose call path was traced but not run is walked through, so it can go here.
- **Consider**: plausible, or real but a judgment call. A real finding that is only stated or
  pointed at the line goes here, with what would raise it, such as "run refund with an amount
  equal to the charge".
- **Noted**: true, but out of scope or minor. One short row each.
- **Dismissed**: wrong or irrelevant. Keep each visible with a one-line reason, so I can
  override.

Rank by verified severity. Every row has a proof level, in Noted and Dismissed too. Agreement
between reviewers counts for little: they share a model's blind spots.
