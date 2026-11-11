# Sources

Step 1 of SKILL.md gathers from each of these. Scope every run with `--project <substring>` and
`--since <YYYY-MM-DD>`.

- **Usage report**: if the harness keeps one, its friction points are known patterns for the
  miners.
- **Corrections**: `scripts/corrections.py` writes each place where I corrected Claude to one
  markdown file. `/hone <skill>` adds `--skill <skill>`; read that skill's SKILL.md and
  references before judging.
- **Review**: the repo's reverts and PR review comments. A correction made in review is a lesson
  too.
- **Lens pass**, in parallel with the correction miners: `scripts/corrections.py --turns` writes
  every turn with its tool calls, to find failures I never noticed and so never corrected.

Split large output into chunks, one per read-only miner. Output small enough to read yourself
still gets every lens.
