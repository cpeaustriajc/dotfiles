# GitHub adapter

Use `gh` (2.94 or later for sub-issues, types and dependencies); `gh auth status` first, and ask
the person to sign in if it fails. Flags: `gh issue create --help`, `gh project --help`.

## Objects

GitHub has no project-with-documents object, so the mapping takes a choice. Ask once which the team
uses, and offer to note the answer in the project's facts; don't edit the project's files unasked.

| Level | GitHub object |
|---|---|
| Product | A Projects board (Projects v2) for the whole product, or a pinned issue |
| Project | A **parent issue** whose sub-issues are its work items, with the project template as its body. On a team that plans in Projects boards, a board per project instead. |
| Spec, engineering document | A wiki page or a pinned issue linked from the parent issue's How. Not a file in the repo: the product owner reads it, and edits shouldn't need a pull request. |
| Decision | Follows the `dossier` skill if installed; otherwise a wiki page per decision |
| Phase | A milestone per project phase, titled `<Project> — <Phase>`, with no due date. On a board, a single-select `Phase` field instead. |
| Work item | Issue |
| Sub-item | Sub-issue (`--parent`) |
| Work type | Issue type (`--type`) when the organisation defines types; otherwise a `Task`, `Bug` or `Chore` label |
| Dependency | Issue dependency (`--blocked-by`, `--blocking`) |
| Cycle | An iteration field on a Projects board, if the team uses one |
| Checklist | Native: `- [ ]` renders and counts toward the issue's progress |
| Status update | A comment on the parent issue, with the health in its first line; or the board's status update |

## Things to know

- **Templates:** `--template` cannot be combined with `--body` and does not take YAML issue
  forms. For a form, or headless, write the body with the form's headings and pass `--body-file`.
- **No `gh milestone` command:** `gh api --method POST repos/{owner}/{repo}/milestones -f title="<Project> — Demo"`.
- **Milestones belong to one repository.** A project spanning repositories uses a Projects board
  with a `Phase` field instead.
- **Closing an issue is not the verifier's Done** unless the team agrees it is. If a pull request
  closes issues on merge (`Closes #n`), say so in the project's facts, and use a label or board
  status for "verified".
- **Every write can notify** watchers and linked channels; batch edits to one issue.
