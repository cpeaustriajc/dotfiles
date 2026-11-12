# GitHub adapter

Tool: `gh` (`gh pr create --help`). Pass `--draft` only when asked. Take reviewers, labels,
assignee, milestone and project from the repo's rules or its recent PRs. Pass `--base` when a
base was given, or the branch was cut from one that exists on origin
(`git ls-remote --heads origin <base>`).

## Upload evidence

- `gh pr create|edit|comment` and `gh issue create|edit|comment` take `--attach ./file` (gh 2.99+,
  push access to the repo). Alt text after `#`: `--attach './before.png#Login error'`.
- Reference the file in the body as `![alt](./before.png)`; gh rewrites the path to a
  `user-attachments` URL. Paths in a `--body-file` are relative to that file's folder, then to the
  working directory.
- Limits: image 10 MB, video 10 MB (Free) or 100 MB (paid plans). For a paid repo, pass the
  limit to `scripts/check-video.sh <file> 100`.
- If one upload fails, gh still creates or updates the PR or issue with the others and exits
  non-zero. Check the exit code and the rendered body, then attach the missing file with
  `gh pr edit --attach`.
- For other file types, or a repo you cannot push to, `gh image` (drogers0/gh-image) can upload,
  but it may read the browser's session cookie. Ask CJ before you use it.
