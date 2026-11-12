# Linear adapter

Use the Linear MCP server (tool list). If the only Linear tools listed are `authenticate` and
`complete_authentication`, ask the person to connect Linear first.

## Objects

| Level | Linear object |
|---|---|
| Product | Initiative |
| Project | Project |
| Spec, engineering document, decision | Project Document (a team-wide decision is a Team Document) |
| Phase | Project milestone |
| Work item | Issue. Linear has no Story, Feature or Epic type. |
| Sub-item | Sub-issue |
| Work type | Issue template (`Task`, `Bug`, `Chore` if the team has them), plus a label |
| Dependency | Issue relation "blocked by"; project dependency for project-level ones |
| Cycle | Cycle |
| Checklist | Native in the editor. A `- [ ]` line sent through the MCP server is unverified: read the item back. |
| Status update | Project update, with health `onTrack`, `atRisk` or `offTrack`; a product update is an initiative update |

Coming from Jira: a Story is an Issue, an Epic is a Project, and an Epic description or Confluence
PRD is the project's spec Document. Never file a spec as an issue, never title a project "Epic 1",
and don't use an `Epic` project template if the workspace has one: the word pulls Jira habits back.

## Things to know

- **Templates:** read the team's template before writing and pass its name on create, so Linear
  applies its labels and fields. A form template's questions are not answered by a description:
  fill its headings in the body. Common ones are a product and an internal-tool project template.
- **No initiative tool listed:** draft the initiative text for the person to paste, and say so;
  never file the product as a project.
- **Relations** (`blockedBy`, `relatedTo`, `parentId` on `save_issue`) only add; removing needs
  the matching `remove…` field. Prefer `patch` over a full `description` for a partial change.
- **Files:** a Linear asset URL needs a Linear sign-in: never embed one in GitHub; upload the
  file there with the GitHub adapter instead.
- **Every write notifies.** Batch changes to one issue into a single `save_issue`.
- **An issue in progress is often frozen** by team convention: put new findings in a comment or a
  new issue. Check the project's facts.
- **Documents have search but no sorted views**, so a hand-kept index rots; find by title search.
- **Done is usually set by the verifier**, sometimes by an integration on merge or review
  request. Don't mark an issue Done for them.
