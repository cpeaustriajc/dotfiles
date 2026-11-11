# Setup and repair

The detail behind each step of `SKILL.md`.

1. Feature files are the map: each has a **Code** line (paths) and **Tests** and **Check** lines
   (proof). New ones go in the verify skill's `references/features/`.
2. Ask the user once where and when the full E2E suite runs. Example: acme's full run took 23-53
   minutes locally. Write the answer into the project's verify skill.
3. The verify skill launches through the project's run skill; it never copies a launch command.
4. Keep the evidence of the first run. Update the skill when a feature file changes.
5. A wrong feature file or verify skill is a renamed route or a moved button: fix that one file
   and say so in the PR. A wrong app is reported, or fixed in the playbooks bug order.
6. Weekly audit and PR verdict: their references hold the steps.
7. Put the proposal at the strongest layer that can hold it: code structure, lint rule, hook,
   test, skill, then instruction file. Route it as in the `hone` skill. Nothing is applied
   silently.

In every step, run the fast checks before the slow ones.
