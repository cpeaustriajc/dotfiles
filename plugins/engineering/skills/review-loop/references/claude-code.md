# Claude Code adapter

- Verify: the project's own verify skill (`Skill` tool). The bundled `/verify` does not count:
  it does not know the project's features. With no project verify skill, the verify step is BLOCKED: say so in the
  report.
- Review: `/code-review high --max-findings all` (`Skill` tool, `skill: "code-review"`), with the
  purpose in the arguments. Take the users from the project's code review rule.
- Simplify: the bundled `/simplify` skill (`Skill` tool, `skill: "simplify"`) on the branch's
  diff. It applies its own fixes.
- Source: https://code.claude.com/docs/en/code-review-local.
