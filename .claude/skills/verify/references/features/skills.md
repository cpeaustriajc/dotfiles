# Skills

What exists: the shipped skills in `plugins/<plugin>/skills/` and this repo's own
`.claude/skills/`. A skill is Markdown plus optional scripts; there is no app to drive.

- **Code:** `plugins/**`; `.claude/skills/**`; `scripts/**`
- **Tests:** `.claude/skills/run-dotfiles/smoke.sh tests` (descriptions, script tests, READMEs)
- **Check:** `claude plugin validate .` exits 0.
