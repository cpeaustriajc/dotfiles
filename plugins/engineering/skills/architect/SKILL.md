---
name: architect
description: "This skill should be used when the user types /architect with a task: sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
disable-model-invocation: true
argument-hint: "<task>"
---

Sketch `$ARGUMENTS` as two designs from two models; code waits for the owner's pick. Open a task
list with one entry per step. Adapters:
`references/claude-code.md`, `../how/references/claude-code.md`.

1. **Ground.** Name the kind: new design, logic re-architecture, or layout
   (`references/layout.md`). Follow `../how/SKILL.md` over each system the code touches, and
   `../why/SKILL.md` when ownership or layering changes. Naming a file isn't grounding; only
   greenfield skips this.
2. **Sketch.** A runner on a second model gets `references/runner-prompt.md`,
   `references/rationale-template.md`, `references/design-red-flags.md`, the task and the
   grounding. Write yours from the same files before reading its result, and never rewrite it
   after. Two whole shapes, not point fixes. Write no file.
3. **Agree.** Show both per `references/agree.md`, recommend one, end the turn and wait.
4. **Pick**: `references/pick.md`. **Push back**: `references/push-back-and-scrap.md`.
5. **Implement.** The sketch is the contract: raise each deviation with the owner.
6. **Scrap.** Repeated friction from the first stub on: `references/push-back-and-scrap.md`.
   Scrap only on the owner's Re-sketch.

## Credit

Adapted from pstack's `architect` by Lauren Tan (MIT; see `LICENSE`).
