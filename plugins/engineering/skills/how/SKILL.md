---
name: how
description: "This skill should be used when the user types /how with a question: \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
argument-hint: "<question>"
---

Answer `$ARGUMENTS` for a senior engineer onboarding onto the subsystem: a working mental model,
not annotated source. Read only; every spawn is read-only. Mechanics: `references/claude-code.md`.

1. **Size**: state your reading of an ambiguous scope. Simple (one module, a narrow question):
   one explainer from `references/explainer-prompt.md` without the findings section, then
   step 4. Complex (several files or services, cross-cutting, an overview): step 2. In doubt,
   simple.
2. **Explore**: 2 to 4 distinct angles, one explorer each from `references/explorer-prompt.md`,
   all in parallel.
3. **Synthesize**: one explainer from `references/explainer-prompt.md` with every explorer's
   findings.
4. **Present** its output with light edits only, in its sections, dropping those that do not
   apply. Complex path: How It Works as a stepper, one box per stage, where a click asks a
   follow-up; with no inline view, a numbered list and a mermaid flowchart.

Adapted from pstack's `how` by Lauren Tan (MIT; see `LICENSE`).
