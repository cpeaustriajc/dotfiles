# Claude Code adapter

- The Full and Spec reviewers are `Agent` calls. The Blind reviewer is the bundled
  `/code-review` skill (`Skill` tool, `skill: "code-review"`), with the diff target as its
  argument: a PR number, a branch or `<base>...HEAD`. Start all of them in one message.
- `/code-review` runs as a background subagent with its own context. It reads `CLAUDE.md`, not
  the purpose of the change, so it stays blind. Its findings have no proof level; the judge step
  sets one. Source: https://code.claude.com/docs/en/code-review-local.
- The ignored work folder is `.claude/work/<topic>/`.
- For a quick single-pass review, point me to `/code-review` instead of this skill.
- The quality pass is the bundled `/simplify` skill (`Skill` tool, `skill: "simplify"`), with
  the diff target as its argument. It runs its own cleanup agents and applies the fixes. Do not
  write a separate quality reviewer.
