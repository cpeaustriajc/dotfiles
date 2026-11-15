# Claude Code: project hooks

Setup steps that copy a hook read this adapter for Claude Code. A cloud session runs the hooks in
the repo's committed `.claude/settings.json`, so the copy goes there, not in `~/.claude`.

- **Hooks folder:** `.claude/hooks/` in the project. Copy each script and its config JSON there,
  flat, with any script it imports.
- **Wiring:** `python3 -I scripts/merge_hooks.py .claude/settings.json <script>.settings.json`
  adds the block once and keeps every entry already there. The commands start with
  `python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/`.
- **Not `.claude/settings.local.json`:** that file is not committed, so a cloud session never
  sees it.
- **Load:** a file watcher normally picks up a hook added to the settings file, in the same
  session. Run the check below to see it load.
- **Where it runs:** a cloud session with one repository runs these hooks. A cloud session with
  several repositories, and a cloud thread in a project, does not; there the skill text alone
  holds the run.
- **Commit:** the copy, the config and the settings change go in one commit of their own, with a
  subject such as `chore: add the <hook> hook`.
- **Check:** pipe one sample event into the copied script and read the decision, for example
  `echo '{"hook_event_name":"PreToolUse","session_id":"setup","tool_name":"Bash","tool_input":{"command":"true"},"cwd":"."}' | python3 .claude/hooks/<script>`
  exits 0 with no deny.
