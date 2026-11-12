# Claude Code adapter

- The comment reader is one `Agent` call with `model` set to the cheapest model the session
  can pick. Paste the output of `git diff <base>...HEAD` and the comment rule into its prompt, so
  it needs no tools and sees nothing of this session.
- `/simplify` and `/code-review` do not replace it: neither checks comments against this rule.
