# Graders and CI

What exists: the files that judge a change. `scripts/graders_changed.py` lists them, and
`.github/workflows/graders.yml` fails a pull request that touches one, so the owner reviews it.
`.github/workflows/checks.yml` runs `smoke.sh validate`, `tests` and `selftest` in CI.

- **Code:** `.github/**`, `scripts/**`, `.claude/skills/verify/**`, `.claude/skills/run-dotfiles/**`,
  `plugins/engineering/skills/review-loop/scripts/**`, `tests/claude-owned/**`
- **Tests:** `smoke.sh selftest`: `scripts/canary.py` and its `--self-test`, and
  `tests/claude-owned/run.py --self-test`; for `.github/**`, `actionlint`.
- **Check:** the pull request names each changed grader, so the owner knows to read it.
