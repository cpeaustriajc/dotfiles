# Sources

Step 1 gathers from each. Scope every run with `--project <substring>` and `--since <YYYY-MM-DD>`.

- **Usage report**: its friction points are known patterns for the miners. If the harness has
  one, I run it (you cannot): read the newest copy. None: mine without it and say it can give one.
- **Corrections**: `scripts/corrections.py` (`--help`); `/hone <skill>` adds `--skill <skill>`
  (read that skill's SKILL.md and references first).
- **Review**: reverts and PR review comments.
- **Lens pass**, parallel to the correction miners: `scripts/corrections.py --turns`, for
  failures never noticed or corrected.

The lens pass uses the correction run's `--project` and `--since` and takes no `--skill`: for
`/hone <skill>`, run without and keep that skill's findings. Its file is about 6 times the
corrections file. Run both with `--chunk-lines 1500`, and have each miner read its chunk in
500-line parts, 150 for the long-lined lens file: a cheap-model miner given more stops early and
reports a partial read as whole, and 500 lens lines overflow its context.

Start all miners in one message, one per chunk, on the cheapest model, read-only; move up one
model when a miner misreads a lens. The missed-trigger lens needs the skill list: this session's
skills plus each project skill's frontmatter.

Missed trigger: a skill-usage report (skills never invoked lately) is a lead, not proof. Proof is
a case in the harness's trigger eval, red before the edit and green after, that checks the named
skill loads on my request.

Output small enough to read yourself still gets every lens.
