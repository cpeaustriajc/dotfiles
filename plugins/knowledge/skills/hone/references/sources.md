# Sources

Step 1 gathers from each. Scope every run with `--project <substring>` and `--since <YYYY-MM-DD>`.

- **Usage report**: its friction points are known patterns for the miners. If the harness has
  one, I run it (you cannot): read the newest copy. None: mine without it and say it can give one.
- **Corrections**: `scripts/corrections.py` (`--help`); `/hone <skill>` adds `--skill <skill>`
  (read that skill's SKILL.md and references first).
- **Review**: reverts and PR review comments.
- **Lens pass**, parallel to the correction miners: `scripts/corrections.py --turns`, for
  failures never noticed or corrected.

Lens pass: use the same `--project` and `--since` as the correction run. It takes no `--skill`:
for `/hone <skill>`, run without and keep only that skill's findings. Its file is about 6 times
the corrections file. Run both with `--chunk-lines 1500` and tell each miner to read its chunk in
500-line parts: a cheap-model miner given more stops early and reports a partial read as whole.
Start the lens miners and correction miners in one message, one per chunk, on the cheapest
model, read-only; move up one model when a miner misreads a lens. The missed-trigger lens needs
the skill list: this session's skills plus each project skill's frontmatter.

Missed trigger: a skill-usage report (skills never invoked lately) is a lead, not proof. Proof is
a case in the harness's trigger eval, red before the edit and green after, that checks the named
skill loads on my request.

Split large output into chunks, one per read-only miner. Output small enough to read yourself
still gets every lens.
