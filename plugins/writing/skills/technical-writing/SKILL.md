---
name: technical-writing
description: >
  This skill should be used when the user types /technical-writing to write, rewrite or review
  a doc, README, RFC, spec, PR description or commit message. It reads the repo's own writing
  rules first, then applies ASD-STE100 sentences.
disable-model-invocation: true
argument-hint: "<the text or file to write, rewrite or review>"
---

# Technical writing

Write so a tired engineer understands on the first read.

1. Read the repo's writing rules: `CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING` and any docs
   style guide. They win over this skill.
2. For a whole document, pick one Diátaxis mode and follow `references/diataxis.md`.
3. Write each sentence by `references/sentence-rules.md`.
4. Rewrite each hit of the `unslop` list, `../unslop/references/patterns.md`. Propose a new
   offender in your reply as a diff to its rule 26, and leave that file unedited.
5. A PR description or a commit message follows every step except step 2. A PR body is a
   one-minute briefing with the evidence that the project's PR rule asks for. Link long logs.
6. Write real paths. Make every count true at the commit that lands it, with the command that
   regenerates it.

Product UI strings follow the product's copy guidelines instead. For one rewrite, before and
after, read `references/worked-example.md`.

## Credit

Adapted from pstack's `technical-writing` by Lauren Tan (MIT; see `LICENSE`).
