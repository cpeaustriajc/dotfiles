---
name: playbooks
description: >
  This skill should be used at the start of a bug fix, refactor, performance problem, feature from
  a ticket, design prototype, or API, module or data-shape design bigger than one line. It routes
  the work to its playbook and proof.
---

Each kind of work fails in its own way, so each has a fixed order that carries its own proof.
Harness mechanics: `references/claude-code.md`.

1. **Pick** one and name it in one line: `references/bug.md`, `refactor.md`, `perf.md`,
   `feature.md`, `prototype.md` or `design.md`. Two kinds (a bug fix that needs a refactor): the
   bug first, the refactor as its own task. None fits (a data migration): write phases, each
   ending in a check, as the playbook.
2. **Copy** its steps verbatim into the task list first. A skipped step stays, marked
   `skip: <reason>`; none drops silently.
3. **Work** them in order. A step that ends in a check is done when the check ran and its
   evidence, per `references/evidence.md`, is saved.
4. **Verdict**: each check ends VERIFIED, NOT VERIFIED or INCONCLUSIVE. INCONCLUSIVE is not a
   pass; missing evidence is a gap.
5. **Report** the proof the playbook asks for, then commit per slice.
