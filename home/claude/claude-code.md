## Claude Code

### Instruction files
- Scope a rule to its files with `paths:`. An `@import` still loads in full.
- Give a custom agent only the instructions its job needs (`omitClaudeMd: true` when it needs
  none of the project's).
- A thread you start asks me nothing itself. It sends its questions and drafts to you, and you ask me.

<!-- Sources: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/best-practices -->
