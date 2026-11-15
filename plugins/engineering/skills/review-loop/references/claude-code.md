# Claude Code: project hooks

A cloud session with one repository runs the hooks in its committed `.claude/settings.json`. A
cloud session with several repositories, or a cloud thread in a project, runs none; there the
skill text alone holds the run.

- **Folder:** `.claude/hooks/`, flat: each script, the scripts it imports, its config JSON.
- **Wire:** `python3 -I scripts/merge_hooks.py .claude/settings.json <script>.settings.json`. It
  adds the block once and keeps the rest. Never `settings.local.json`: it is not committed.
- **Commit:** all of it in one commit, such as `chore: add the <hook> hook`.
- **Check:** pipe a sample event into the copy; it exits 0 with no deny:
  `echo '{"hook_event_name":"PreToolUse","session_id":"setup","tool_name":"Bash","tool_input":{"command":"true"},"cwd":"."}' | python3 .claude/hooks/<script>`
