## Claude Code

### Instruction files
- Scope a rule to its files with `paths:`. An `@import` still loads in full.
- Give a custom agent only the instructions its job needs (`omitClaudeMd: true` when it needs
  none of the project's).
- A thread you start asks me nothing itself. It sends its questions and drafts to you, and you ask me.
- Start each thread on the cheapest model that fits, at `medium` effort: Haiku 5.5 for mechanical
  work, Sonnet 5.5 for specced work, Opus 5.5 for design. Fable 5.2 only on my word.
- A thread's report ends with what it ran and what the brief missed. Brief too small? Split the task
  by the project's workflow.

<!-- Sources: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/best-practices -->
