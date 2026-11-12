# Sources

Step 1 gathers from each. Scope every run with `--project <substring>` and `--since <YYYY-MM-DD>`.

- **Usage report**: its friction points are known patterns for the miners.
- **Corrections**: `scripts/corrections.py` writes each correction to one markdown file;
  `/hone <skill>` adds `--skill <skill>` (read that skill's SKILL.md and references first).
- **Review**: reverts and PR review comments.
- **Lens pass**, parallel to the correction miners: `scripts/corrections.py --turns`, every turn
  with its tool calls, for failures never noticed or corrected.

Split large output into chunks, one per read-only miner. Output small enough to read yourself
still gets every lens.
