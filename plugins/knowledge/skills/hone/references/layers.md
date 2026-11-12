# Layers

Step 4 of SKILL.md routes each lesson to the first layer that can hold it.

1. **Code structure**: make the wrong thing impossible to write. Claude copies the nearest
   example, so delete or fix a stale one instead of adding a rule against it.
2. **Lint, typecheck or CI rule**, ratcheted when the bad pattern is already common; same command
   locally and in CI, with an actionable error.
3. **Hook**, for a tool-use pattern ("never X on main").
4. **Test**: end-to-end, for a regressed behaviour.
5. **Skill**: a lesson about one skill goes into its own SKILL.md or references, never a general
   file; edit the covering skill before writing a new one. A missed trigger edits the description
   and adds my request as a should-trigger case, proven with the harness's trigger eval.
6. **Agent definition.**
7. **Instruction file** (CLAUDE.md, AGENTS.md, `paths:`-scoped rule): rules and preferences only,
   one line each, never a status, date or finding. A rule needing judgment carries one short
   failure example.

A structural fix that holds also deletes the instruction it replaces. Any exception or
suppression a proposal adds carries an expiry (date or issue), in the code or config, never an
instruction file.
