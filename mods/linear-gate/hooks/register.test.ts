import { expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'
import type { Engine } from 'claude-code/testing'

// On shift in UTC, onShift 'ask': every Linear write gets the mod's own ask.
type Body = ($: Engine, on: On) => unknown
const asking = (name: string, body: Body) =>
  test(name, { options: { timeZone: 'UTC', onShift: 'ask' } }, (($: Engine, on: On) => {
    on('clock.now', () => ({ value: Date.UTC(2026, 9, 15, 10) }) as never)
    return body($, on)
  }) as never)

const LINEAR = 'mcp__linear-server__'
const LINEAR_CONNECTOR = 'mcp__c52a7905-a861-4431-9619-0e85c0e83d6a__'

function ran(on: On) {
  const tools: string[] = []
  on('tool.call', (_$, e) => {
    tools.push(e.tool)
    return { result: 'ok' } as never
  })
  return tools
}

async function verdict($: Engine, call: Record<string, unknown>) {
  const { tool, ...input } = call
  return $.tool.check({ tool, input } as never)
}

// The headline the person reads: the reason, without the mod's name.
async function headline($: Engine, call: Record<string, unknown>) {
  const v = await verdict($, call)
  expect(v.decision).toBe('ask')
  return (v.reason ?? '').replace(/^linear-gate: /, '')
}

const comment = { tool: `${LINEAR}save_comment`, issueId: 'ACME-77', body: 'Notice: AC 3 cannot ship as written.' }

asking('a Linear write is asked of a person and names the mod', async $ => {
  const v = await verdict($, comment)
  expect(v.decision).toBe('ask')
  expect(v.plugin).toBe('linear-gate')
  expect(v.reason).toBe('linear-gate: Comment on issue ACME-77.')
})

asking('where nobody can answer the ask, the write never runs', async ($, on) => {
  const tools = ran(on)
  const out = await $.tool.call(comment as never)
  expect(out.isError).toBe(true)
  expect(tools).toEqual([])
})

asking('a subagent write is gated', async ($, on) => {
  const tools = ran(on)
  await $.tool.call({ ...comment, agentId: 'a1' } as never)
  expect(tools).toEqual([])
})

asking('Linear reads are left to the host', async ($, on) => {
  const tools = ran(on)
  await $.tool.call({ tool: `${LINEAR}get_issue`, id: 'ACME-77' } as never)
  await $.tool.call({ tool: `${LINEAR_CONNECTOR}list_issues`, team: 'Acme' } as never)
  expect(tools.length).toBe(2)
  expect((await verdict($, { tool: `${LINEAR}get_issue`, id: 'ACME-77' })).plugin).toBe(undefined)
})

asking('the claude.ai Linear connector is gated too', async $ => {
  expect((await verdict($, { ...comment, tool: `${LINEAR_CONNECTOR}save_comment` })).decision).toBe('ask')
})

asking('a write on a future linear-server tool is gated', async $ => {
  expect((await verdict($, { tool: `${LINEAR}update_cycle`, id: 'c1' })).decision).toBe('ask')
})

asking('look-alike writes on other servers are left to the host', async $ => {
  for (const tool of ['mcp__github__update_issue', 'mcp__notion__create_page', 'Bash'])
    expect((await verdict($, { tool, id: 'x' })).plugin).toBe(undefined)
})

const newIssue = { tool: `${LINEAR}save_issue`, team: 'Acme', title: 'Fix cart total', description: '## Context' }
const pr = 'acme/app#415'
const reply = { tool: `${LINEAR}save_comment`, parentId: '9cfdbd28-6d4e-4d7a-af39-daa8dd6f279b', body: 'Done.' }

const headlines: [string, Record<string, unknown>, string][] = [
  ['a new issue names its team, title and template', { ...newIssue, template: 'Chore' }, 'Create issue "Fix cart total" in Acme with template Chore.'],
  ['a new issue without a template says so', newIssue, 'Create issue "Fix cart total" in Acme with no template.'],
  ['an issue update names the issue, not a template', { tool: `${LINEAR}save_issue`, id: 'ACME-123', state: 'In Progress' }, 'Update issue ACME-123.'],
  ['an issue moved to Done says so', { tool: `${LINEAR}save_issue`, id: 'ACME-9', state: 'Done' }, 'Complete issue ACME-9.'],
  ['a review request names the reviewer and the PR', { tool: `${LINEAR}update_diff`, urlOrId: pr, addedReviewRequests: [{ user: 'Codex' }] }, 'Request review from Codex on PR acme/app#415.'],
  ['a PR status change says what the status becomes', { tool: `${LINEAR}update_diff`, urlOrId: pr, statusAction: 'markReadyForReview' }, 'Mark PR acme/app#415 ready for review.'],
  ['a PR edit joins its changes', { tool: `${LINEAR}update_diff`, urlOrId: pr, addedIssueLinks: [{ issue: 'ACME-123', type: 'closes' }], statusAction: 'close' }, 'Link ACME-123 (closes) to PR acme/app#415; Mark PR acme/app#415 closed.'],
  ['a merge names the PR and the method', { tool: `${LINEAR}merge_diff`, urlOrId: pr, mergeMethod: 'SQUASH' }, 'Merge PR acme/app#415 (squash).'],
  ['a review decision is spelled out', { tool: `${LINEAR}submit_diff_review`, urlOrId: pr, decision: 'approved' }, 'Approve PR acme/app#415.'],
  ['a reply says it is a reply, with no raw comment id', reply, 'Reply to a comment.'],
  ['a reply that names its issue says where it lands', { ...reply, issueId: 'ACME-77' }, 'Reply to a comment on issue ACME-77.'],
  ['an edited comment names it by a short id', { tool: `${LINEAR}save_comment`, id: '9cfdbd28-6d4e-4d7a-af39-daa8dd6f279b', body: 'x' }, 'Edit comment 9cfdbd28….'],
  ['a new status update names the project and its health', { tool: `${LINEAR}save_status_update`, type: 'project', project: 'ACME Checkout', health: 'atRisk' }, 'Post a project status update on ACME Checkout, health at risk.'],
  ['an edit of a posted status update says it edits one', { tool: `${LINEAR}save_status_update`, type: 'initiative', id: 'su1', health: 'onTrack' }, 'Edit the posted initiative status update su1, health on track.'],
  ['a comment on a status update reads as one', { tool: `${LINEAR}save_comment`, statusUpdateId: 'su1', body: 'x' }, 'Comment on status update su1.'],
  ['a new label names its team', { tool: `${LINEAR}create_issue_label`, name: 'bug', teamId: 'Acme' }, 'Create issue label "bug" in team Acme.'],
  ['a workspace label says it has no team', { tool: `${LINEAR}create_issue_label`, name: 'bug' }, 'Create issue label "bug" for the whole workspace.'],
  ['a label edit reads as a sentence', { tool: `${LINEAR}save_project_label`, id: 'l1', name: 'x' }, 'Edit project label l1.'],
  ['a label restore reads as a sentence', { tool: `${LINEAR}restore_issue_label`, id: 'l1' }, 'Restore issue label l1.'],
  ['a new project names itself', { tool: `${LINEAR}save_project`, name: 'ACME Checkout', team: 'ACME' }, 'Create project "ACME Checkout".'],
  ['a new document names itself', { tool: `${LINEAR}save_document`, title: 'Decision: Cart', project: 'ACME Checkout' }, 'Create document "Decision: Cart".'],
  ['a thread resolve names the thread', { tool: `${LINEAR}resolve_diff_thread`, threadId: 't1' }, 'Resolve PR thread t1.'],
  ['an unknown write reads as words and names its tool', { tool: `${LINEAR}share_issue`, id: 'ACME-1' }, 'Share issue (share_issue).'],
]

for (const [name, call, line] of headlines)
  asking(name, async $ => expect(await headline($, call)).toBe(line))

const drastic: [string, Record<string, unknown>, string][] = [
  ['an issue moved to Canceled', { tool: `${LINEAR}save_issue`, id: 'ACME-9', state: 'Canceled' }, 'Cancel issue ACME-9.'],
  ['a project cancel', { tool: `${LINEAR}save_project`, id: 'P-ACME-7', state: 'Canceled' }, 'Cancel project P-ACME-7.'],
  ['a status update delete', { tool: `${LINEAR}delete_status_update`, type: 'project', id: 'su1' }, 'Delete the project status update su1.'],
  ['a label retire', { tool: `${LINEAR}retire_issue_label`, id: 'l1' }, 'Retire issue label l1.'],
  ['a comment delete', { tool: `${LINEAR}delete_comment`, id: 'c1' }, 'Delete comment (delete_comment).'],
]

for (const [name, call, line] of drastic)
  asking(`${name} warns that the team sees it`, async $ =>
    expect(await headline($, call)).toBe(`${line} Everyone on the team sees this.`))

asking('a plain edit carries no warning', async $ => {
  expect(await headline($, { tool: `${LINEAR}save_project`, id: 'P-ACME-7', state: 'Started' })).not.toMatch(/Everyone/)
})

const DOC = 'c089f90f-1b2c-4d5e-8f90-123456789abc'
const edit = { tool: `${LINEAR}save_document`, id: DOC, patch: [{ op: 'append', text: 'x' }] }

function lookups(on: On, lookup: 'title' | 'error' | 'throw' | 'garbage' | 'hang') {
  const looked: string[] = []
  on('mcp.call', (_$, e) => {
    looked.push(`${e.server}/${e.tool}/${String(e.args.id)}`)
    if (lookup === 'throw') throw new Error('offline')
    if (lookup === 'hang') return new Promise(() => {}) as never
    const text = lookup === 'garbage' ? 'not json' : JSON.stringify({ id: DOC, title: 'Decision: Cart' })
    return { value: { content: [{ type: 'text', text }], isError: lookup === 'error' } } as never
  })
  return looked
}

asking('a document edit names the document by its title', async ($, on) => {
  const looked = lookups(on, 'title')
  expect(await headline($, edit)).toBe('Update document "Decision: Cart".')
  expect(looked).toEqual([`linear-server/get_document/${DOC}`])
})

for (const lookup of ['error', 'throw', 'garbage', 'hang'] as const) {
  asking(`a failed title lookup (${lookup}) falls back to the short id`, async ($, on) => {
    if (lookup === 'hang') on('clock.sleep', () => ({ value: undefined }) as never)
    lookups(on, lookup)
    expect(await headline($, edit)).toBe('Update document c089f90f….')
  })
}

asking('a new document makes no lookup', async ($, on) => {
  const looked = lookups(on, 'title')
  await verdict($, { tool: `${LINEAR}save_document`, title: 'New', project: 'P' })
  expect(looked).toEqual([])
})
