# dotfiles

- Trunk-based development, no PRs: this overrides the global rules. `/verify` before each
  push (`python3 -I scripts/check_trunk.py`).
- Each rule names its failure. When a frontier model or vendor best-practice post ships, audit and
  cut rules the model no longer needs.

## Writing

- No AI slop: state findings and cite the check. Failure: declauding's corpus counts slop PR
  descriptions at 0.70% in early 2025 and 39.5% in August 2026.

## Instructions for a model

- Name a known term instead of explaining it. Give reasons, not MUST or all caps: newer models
  over-apply them. A rule that must always hold needs a check.

## Build only what the tools lack

- No Not-Invented-Here: read the harness, code host, CI and tracker docs and changelog first;
  build only the missing part. Failure: `hone` re-mined what `/insights` and auto memory mine.
- Hand off only to stable features; a guard only to one that always holds.
- Prior art: evidence over authority. Cite source and evidence in the README. `SOURCES.md` holds
  leads.

## Authoring

- Check `SCOPE.md`. YAGNI on fan-out: only for parallel work or fresh context. Cheapest capable
  model (`models/README.md`).
- After a change, run `run-dotfiles` and audit the edit (`.claude/rules/claude-code-authoring.md`).
  Move a still-needed rule; never drop it.

## Layout

- `.claude-plugin/marketplace.json` is the only manifest. A mod's `.claude-plugin/plugin.json`
  holds only `name`, `types`, `userConfig`; without it validate and test skip them (linear-gate
  failed 86 of 105 tests).
- Skills: `plugins/<plugin>/skills/<skill>/`. Mods: `mods/<mod>/`. Retire one by deleting its
  folder in a commit that names it.
- Each has a README for people (`.claude/rules/wiki.md`, `scripts/check_readmes.py`).
- Move a skill in one commit: `git mv`, update README rows, bump both plugins' versions, validate.

## Tool-neutral

- Method in the skill, mechanics in `references/<tool>.md`, team taste in the team's repo. No
  tracker terms (`scripts/check_tracker_terms.py`).
- A typed skill needs `agents/openai.yaml` with `allow_implicit_invocation: false`, or Codex
  starts it (`scripts/check_typed_skills.py`).
- A mod adds only what the harness lacks; never override its permissions, settings or classifier
  (`tests/claude-owned/run.py`).
- Single source of truth: no hand copies in `~/.claude/skills` or `.agents/skills`.

## home-manager

- `home/claude/` is `~/.claude`. Public repo: no secrets, no machine state.
- Generated files change only after `home-manager switch --flake ~/Projects/dotfiles#cj` (needs
  `/nix/var/nix/profiles/default/bin` and `~/.nix-profile/bin` on `PATH`).
- `settings.json` syncs only `settings.shared.json` keys; capture live edits with
  `home/claude/settings-capture.sh`.
