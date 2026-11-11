---
name: formal-verify
description: >
  This skill should be used when the user says "model-check this race", "prove this invariant",
  "formally verify this" or "is the model still true to the code", or when a retry, race, lease or
  state machine needs more than tests. It writes or maintains a project verify skill.
---

A race passes every written test; a model checker tries every order. A formal check exists and
the code changed since its sync commit: `references/maintain.md`. Otherwise:

1. **Target**: the promise whose break harms users most and that tests reach least, not the
   easiest one. Ask only what the code cannot say.
2. **Tool**: event order gets TLA+ on a small model; every input gets a verifier on the code,
   else generated-input tests on the real code.
3. **Model**: each part points to code; one atomic code step is one model step; repo names.
4. **Able to fail**: each property fails on a broken variant first. An unseen failure proves
   nothing.
5. **Findings stay findings**: report a break in the current code as steps in the code's words,
   with its harm. Never weaken the property or model to pass; product code changes only when
   asked.
6. **Verify skill** per `references/verify-skill.md`.
7. **Prove it**: break the real code, follow the verify skill as the next agent would, see it
   catch the break, then drop the break and confirm the start state. A miss fixes the skill
   or model, not the break.
8. **Hand off** per `references/verify-skill.md`.
