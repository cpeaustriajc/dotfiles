# Playwright

Mechanics for the hero-script video in `evidence.md`; read the current Playwright docs for the
`screencast` API (`show_actions`, `show_chapter`).

- Playwright draws no click mark unless `show_actions` is given a styled `point`. The repo's
  style: `cursor="pointer"`, `title` hidden, `point` a 28px circle with a 3px red border. Add a key
  label of your own.
- If `screencast` is missing, the installed Playwright is older than these calls: upgrade it or
  use the project's own helper.
