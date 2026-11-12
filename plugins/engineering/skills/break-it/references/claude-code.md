# Claude Code

- Launch with `/run`. It follows the project's recorded recipe when one exists
  (`.claude/skills/run-<name>/`, from `/run-skill-generator`), else guesses from the project type
  and the README, `package.json` or `Makefile`.
- The guess is unreliable when the app needs a database, an env file or a multi-step build.
- `/run` and `/verify` show the happy path. The careless users start only when the app is up.

Source: https://code.claude.com/docs/en/skills, section "Run and verify your app".
