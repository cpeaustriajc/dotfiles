# Behaviour

What exists: `evals/behaviour/<case>/` checks that a skill changes what Claude does, scored with
the plugin and without it.

- **Code:** `evals/behaviour/<case>/**`; each changed case is its own feature.
- **Tests:** `CASE=<case> .claude/skills/run-dotfiles/smoke.sh behaviour` (about $0.40 a case).
- **Check:** the report shows Δ above 0 for the case: the plugin arm passes, the baseline fails.
