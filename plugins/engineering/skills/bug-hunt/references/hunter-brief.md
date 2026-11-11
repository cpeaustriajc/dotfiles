# Hunter brief

Step 2 of `SKILL.md` sends this brief to each hunter. Fill in the brackets.

> Goal: find real bugs in [scope] and fix the ones in your shard [file list].
> A bug is wrong behaviour, a regression, a broken edge case, a security hole, data loss or a
> divergence from [spec/issue]. Not style, naming, "consider adding" or a refactor.
> Known bugs already fixed or rejected: [ledger]. Do not report them again.
> Test command: [test command]. E2E command: [E2E command]. Rules on test ids and copy: [rules].
> For each bug in your shard: write a test that fails, show it fail, fix the code, show it pass.
> Follow the bug order in the `playbooks` skill.
> Do not change test ids or visible copy unless the fix needs it. If you cannot write a failing
> test, do not fix it: report it as unproven.
> For a bug outside your shard: report it, do not edit.
> Read every file in your shard in full. Return: one line per shard file (`path: clean` or
> `path: N bugs`), then per bug: file:line, the defect, the failure scenario (input or state →
> wrong result), the test name, fixed or not and why. End with `BUGS FOUND: <n>`.
