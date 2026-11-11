# Layers

Step 4 of SKILL.md routes each lesson to the first layer in this list that can hold it.

1. **Code structure**: make the wrong thing impossible to write (a type, a boundary, one shared
   helper). Claude copies the nearest example, so when it copied a stale one, delete or fix that
   example instead of adding a rule against it.
2. **Lint, typecheck or CI rule**. When the bad pattern is already common, ratchet it: the check
   fails only on a change that adds more. The same command runs locally and in CI. The error
   message names the fix as well as the problem.
3. **Hook**, for a tool-use pattern such as "never X on main".
4. **Test**: an end-to-end check, for a behaviour that regressed.
5. **Skill**: a procedure or a domain's know-how. A lesson about one skill goes into that skill's
   own SKILL.md or references, never a general instruction file. Edit the skill that covers it
   before you write a new one. A missed trigger edits the skill's description and adds my request
   as a should-trigger case, proven with the harness's trigger eval.
6. **Agent definition**: the harness's agent files, or a plugin's agents.
7. **Instruction file**: CLAUDE.md, AGENTS.md or a `paths:`-scoped rule. Only rules and
   preferences go here, one line each, never a status, a date or a finding. Keep each
   always-loaded file under the harness's size limit. A rule that needs judgment carries one
   short example of the failure.

A structural fix that holds also deletes the instruction it replaces.

Any exception or suppression a proposal adds carries an expiry, such as a date or an issue to
remove it. Put it in the code or config it applies to, never in an instruction file.
