# GitHub adapter

Tool: `gh` (`gh pr create --help`), with `--body-file` for the checked body. Pass `--base` when a
base was given, or the branch was cut from one that exists on origin
(`git ls-remote --heads origin <base>`).

## Upload evidence

- `--attach ./file` on `gh pr|issue create|edit|comment` (gh 2.99+, push access; `--help`). Reference
  the file in the body as `![alt](./before.png)`, relative to the body file's folder.
- Video limit: 10 MB (Free) or 100 MB (paid plans): pass it as `scripts/check-video.sh <file> 100`.
- If one upload fails, gh still creates or updates the PR or issue with the others and exits
  non-zero. Check the exit code and the rendered body, then attach the missing file with
  `gh pr edit --attach`.
- For other file types, or a repo you cannot push to, `gh image` (drogers0/gh-image) can upload,
  but it may read the browser's session cookie. Ask the user before you use it.
