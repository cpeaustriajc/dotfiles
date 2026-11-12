# Gotchas

- `--plugin-dir .` loads no dotfiles skill: the repo root is a marketplace, not a plugin.
  Install from the local marketplace, as `smoke.sh` does.
- `claude plugin validate` on a skill folder always fails with "No manifest found". Validate
  the repo root.
- `doctor` exits 2 (`BLOCKED`) without `CLAUDE_CODE_OAUTH_TOKEN` or a 1Password sign-in: a
  fresh config directory is signed out on macOS.
- The 7-day token and use columns are always empty in the temporary config. For real usage,
  run `claude -p "/skill-doctor"` with your own config.
- Write a description as a `>` block scalar. An unquoted one that contains `": "` is invalid
  YAML that `claude plugin validate` misses.
- `tests_kept.py` has no allow file. When it flags a test that is truly wrong, stop and tell the
  owner which test and why; the owner merges past it.
- `selftest` copies only the files git lists (`git ls-files -co --exclude-standard`), so a runner
  rigged through an ignored file shows up in CI, not here.
