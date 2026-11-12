# Claude Code

Docs: https://code.claude.com/docs/en/costs, "Analyze your usage patterns" (`/insights`).

## Ask tool

Step 6: `AskUserQuestion`, one option per proposal, `multiSelect: true`.

## Layers

Hooks: write them with the `update-config` skill.

## Usage report

- I type `/insights`; Claude does not run it. Read the newest `~/.claude/usage-data/report.html`
  (or its timestamped copies). None: mine without it and say `/insights` can give one.

## Instruction-file audit

- `/doctor prompt-audit [path]` reports and edits nothing. Headless:
  `claude -p "/doctor prompt-audit" --add-dir ~/.claude`, the flag after the prompt (it takes
  several paths).
- It reports installed plugin skills without proposing edits: audit the skill's source path.
- `claude-md-improver` (claude-md-management): stale commands and paths are prune candidates; its
  additions still pass step 2.
- An always-loaded file over 200 lines loses adherence (docs: "Memory", `code.claude.com/docs/en/memory`).
- `/revise-claude-md` output is single-run corrections until they recur.

## Lens pass

- `scripts/corrections.py --turns` with the same `--project` and `--since` as the correction run
  (`--help` has the flags). It takes no `--skill`: for `/hone <skill>`, run without and keep only
  that skill's findings. The file is about 6 times the corrections file.
- `--chunk-lines 1500` on both runs. Tell each miner to read its chunk in 500-line parts: a
  cheap-model miner given more stops early and reports a partial read as whole.
- Start lens subagents and correction miners in one message, one `Agent` per chunk on the
  cheapest model, read-only. Move up one model when a miner misreads a lens.
- Missed-trigger lens skill list: this session's skills listing plus each
  `.claude/skills/*/SKILL.md` frontmatter in the project.

## Missed trigger proof

Use what Claude Code ships; hone adds only the transcript evidence of the missed request.
- `/skill-doctor` (skills never invoked in 7 days) is a lead, not proof.
- skill-creator's description loop (`scripts/run_loop.py --eval-set <triggers.json>`): add the
  request to the skill's `evals/triggers.json` as `"should_trigger": true`; apply `best_description`
  by hand.
- Proof: a `claude plugin eval <plugin> --case <case>` case in `evals/` (`prompt.md` plus a
  `tool_used` grader on `Skill` with `input_match` naming the skill), red before the edit and green
  after. It does not read `triggers.json`.
