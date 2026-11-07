import type { EngineInterface, Register } from 'claude-code'

const LINEAR_WRITES = new Set([
  'save_issue', 'save_comment', 'save_document', 'save_project', 'save_milestone',
  'save_initiative', 'save_initiative_label', 'save_issue_label', 'save_project_label',
  'save_release', 'save_release_note', 'save_status_update', 'save_diff_comment',
  'create_attachment', 'create_attachment_from_upload', 'create_issue_label',
  'create_initiative_label', 'delete_attachment', 'delete_comment', 'delete_diff_comment',
  'delete_status_update', 'merge_diff', 'update_diff', 'submit_diff_review',
  'resolve_diff_thread', 'retire_issue_label', 'retire_initiative_label',
  'retire_project_label', 'restore_issue_label', 'restore_initiative_label',
  'restore_project_label', 'share_issue', 'unshare_issue', 'mark_notification',
])
const LINEAR_SERVER_WRITE = /^(save|delete|create|update|merge|submit|resolve|retire|restore|share|unshare|mark)_/
const LOOKUP_MS = 3000
const DEFAULT_START = '09:00'
const DEFAULT_END = '18:00'
const ON_SHIFT = new Set(['host', 'drastic', 'ask'])

function minutesOf(v: unknown): number | undefined {
  const m = typeof v === 'string' ? /^([01]\d|2[0-3]):([0-5]\d)$/.exec(v) : null
  return m ? Number(m[1]) * 60 + Number(m[2]) : undefined
}

function minuteOfDay(ms: number, zone: string | undefined): number {
  const [h, m] = new Intl.DateTimeFormat('en-US', { timeZone: zone, hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
    .format(new Date(ms)).split(':').map(Number)
  return h * 60 + m
}

const inShift = (now: number, start: number, end: number) =>
  start <= end ? now >= start && now < end : now >= start || now < end

function linearWrite(tool: string): string | undefined {
  const m = /^mcp__(.+?)__(.+)$/.exec(tool)
  if (!m) return undefined
  const [, server, name] = m
  if (LINEAR_WRITES.has(name)) return name
  if (server === 'linear-server' && LINEAR_SERVER_WRITE.test(name)) return name
  return undefined
}

const PR_STATUS: Record<string, string> = {
  markReadyForReview: 'ready for review', convertToDraft: 'back to draft', close: 'closed', reopen: 'reopened',
}
const REVIEW: Record<string, string> = { approved: 'Approve', changesRequested: 'Request changes on', commented: 'Leave a review comment on' }

const HEALTH: Record<string, string> = { onTrack: 'on track', atRisk: 'at risk', offTrack: 'off track' }
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
const short = (v: string) => (UUID.test(v) ? `${v.slice(0, 8)}…` : v)
const words = (k: string) => k.replace(/Id$/, '').replace(/([A-Z])/g, ' $1').replace(/_/g, ' ').toLowerCase().trim()
const FIELD: Record<string, string> = { state: 'Status' }
const heading = (k: string) => FIELD[k] ?? words(k).replace(/^./, c => c.toUpperCase())
const STATE_VERB: Record<string, string> = { canceled: 'Cancel', cancelled: 'Cancel', done: 'Complete', completed: 'Complete' }
const people = (v: unknown) =>
  (Array.isArray(v) ? v : []).map(r => String(r.user ?? r.externalUserId ?? r.githubTeamId)).join(', ')

function whatItDoes(name: string, a: Record<string, unknown>): [string[], string[]] {
  const s = (k: string) => (typeof a[k] === 'string' ? (a[k] as string) : undefined)
  const pr = `PR ${s('urlOrId')}`
  switch (name) {
    case 'save_issue': {
      if (s('id')) return [[`${STATE_VERB[s('state')?.toLowerCase() ?? ''] ?? 'Update'} issue ${short(s('id')!)}`], ['id']]
      const template = s('template') ? `with template ${s('template')}` : 'with no template'
      return [[`Create issue "${s('title')}" in ${s('team')} ${template}`], ['title', 'team', 'template']]
    }
    case 'save_comment': {
      const parent = ['issueId', 'projectId', 'documentId', 'initiativeId', 'milestoneId', 'statusUpdateId'].find(k => s(k))
      const noun = parent?.replace(/Id$/, '').replace(/([A-Z])/g, ' $1').toLowerCase()
      const where = parent ? ` on ${noun} ${short(s(parent)!)}` : ''
      if (s('id')) return [[`Edit comment ${short(s('id')!)}`], ['id', ...(parent ? [parent] : [])]]
      if (s('parentId')) return [[`Reply to a comment${where}`], ['parentId', ...(parent ? [parent] : [])]]
      return parent ? [[`Comment${where}`], [parent]] : [[], []]
    }
    case 'save_status_update': {
      const health = s('health') ? `, health ${HEALTH[s('health')!] ?? s('health')}` : ''
      const lines = s('id')
        ? [`Edit the posted ${s('type')} status update ${s('id')}${health}`]
        : [`Post a ${s('type')} status update on ${s('project') ?? s('initiative')}${health}`]
      return [lines, ['type', 'id', 'health', 'project', 'initiative']]
    }
    case 'save_project': case 'save_milestone': case 'save_initiative': case 'save_document': {
      const noun = name.split('_')[1]
      if (s('id')) return [[`${STATE_VERB[s('state')?.toLowerCase() ?? ''] ?? 'Update'} ${noun} ${short(s('id')!)}`], ['id']]
      const key = s('name') ? 'name' : 'title'
      return [[`Create ${noun} "${s(key)}"`], [key]]
    }
    case 'delete_status_update':
      return [[`Delete the ${s('type')} status update ${s('id')}`], ['type', 'id']]
    case 'update_diff': {
      const lines: string[] = []
      if (a.addedReviewRequests) lines.push(`Request review from ${people(a.addedReviewRequests)} on ${pr}`)
      if (a.removedReviewRequests) lines.push(`Withdraw the review request to ${people(a.removedReviewRequests)} on ${pr}`)
      for (const l of (Array.isArray(a.addedIssueLinks) ? a.addedIssueLinks : []) as { issue: string; type: string }[])
        lines.push(`Link ${l.issue} (${l.type}) to ${pr}`)
      if (a.removedIssueLinks) lines.push(`Unlink ${(a.removedIssueLinks as string[]).join(', ')} from ${pr}`)
      if (s('statusAction')) lines.push(`Mark ${pr} ${PR_STATUS[s('statusAction')!] ?? s('statusAction')}`)
      if (!lines.length) lines.push(`Edit ${pr}`)
      return [lines, ['urlOrId', 'addedReviewRequests', 'removedReviewRequests', 'addedIssueLinks', 'removedIssueLinks', 'statusAction']]
    }
    case 'merge_diff':
      return [[`Merge ${pr}${s('mergeMethod') ? ` (${s('mergeMethod')!.toLowerCase()})` : ''}`], ['urlOrId', 'mergeMethod']]
    case 'submit_diff_review':
      return [[`${REVIEW[s('decision') ?? ''] ?? 'Review'} ${pr}`], ['urlOrId', 'decision']]
    case 'save_diff_comment': {
      const verb = a.draft ? 'Save a draft comment on' : s('commentId') ? 'Edit a comment on' : s('parentId') ? 'Reply on' : 'Comment on'
      return [[`${verb} ${pr}`], ['urlOrId', 'draft', 'commentId', 'parentId', 'draftId', 'anchor', 'anchorContent']]
    }
    case 'create_issue_label': case 'create_initiative_label':
    case 'save_issue_label': case 'save_initiative_label': case 'save_project_label': {
      const noun = `${name.split('_')[1]} label`
      if (name.startsWith('save_') && s('id')) return [[`Edit ${noun} ${s('id')}`], ['id']]
      const where = s('teamId') ? `in team ${short(s('teamId')!)}` : 'for the whole workspace'
      return [[`Create ${noun} "${s('name')}" ${where}`], ['name', 'teamId']]
    }
    case 'retire_issue_label': case 'retire_initiative_label': case 'retire_project_label':
    case 'restore_issue_label': case 'restore_initiative_label': case 'restore_project_label': {
      const [verb, kind] = name.split('_')
      return [[`${heading(verb)} ${kind} label ${s('id') ?? s('name')}`], ['id', 'name']]
    }
    case 'resolve_diff_thread':
      return [[`${a.resolved === false ? 'Reopen' : 'Resolve'} PR thread ${s('threadId')}`], ['threadId', 'resolved']]
    default:
      return [[], []]
  }
}

function actionOf(name: string, args: Record<string, unknown>): string {
  const [lines] = whatItDoes(name, args)
  return lines.length ? lines.join('; ') : `${heading(name)} (${name})`
}

function isDrastic(name: string, args: Record<string, unknown>): boolean {
  return /^(delete|retire)_/.test(name) || STATE_VERB[String(args.state).toLowerCase()] === 'Cancel'
}

async function documentTitle($: EngineInterface, server: string, id: string): Promise<string | undefined> {
  try {
    const timeout = $.clock.sleep(LOOKUP_MS).then(() => undefined, () => new Promise<never>(() => {}))
    const out = await Promise.race([$.mcp.call(server, 'get_document', { id }), timeout])
    if (!out || out.isError) return undefined
    for (const block of out.content) {
      if (block.type !== 'text') continue
      const title = (JSON.parse((block as { text: string }).text) as { title?: unknown }).title
      if (typeof title === 'string' && title) return title
    }
  } catch {
    return undefined
  }
  return undefined
}

export const register: Register = (on, options) => {
  const set = minutesOf(options.shiftStart) !== undefined && minutesOf(options.shiftEnd) !== undefined
  const [from, to] = set ? [options.shiftStart as string, options.shiftEnd as string] : [DEFAULT_START, DEFAULT_END]
  const [start, end] = [minutesOf(from)!, minutesOf(to)!]
  const zone = typeof options.timeZone === 'string' && options.timeZone ? options.timeZone : undefined
  const onShift = ON_SHIFT.has(options.onShift as string) ? (options.onShift as string) : 'drastic'

  on('tool.call', async ($, e, next) => {
    if (!linearWrite(e.tool)) return next(e)
    if (inShift(minuteOfDay(await $.clock.now(), zone), start, end)) return next(e)
    return { deny: `${$.plugin.name}: off shift (${from}-${to}); a Linear write notifies the team's Slack. Do not retry: draft it in the chat for the next shift.` }
  })

  // An ask a hook makes is a person's: the dialog, the host's callback or a PermissionRequest
  // hook answers it, no auto-mode allow settles it, and where nobody can be asked it is a deny.
  on('tool.check', async ($, e, next) => {
    const name = linearWrite(e.tool)
    if (!name) return next(e)
    let args = (e.input ?? {}) as Record<string, unknown>
    if (onShift === 'host' || (onShift === 'drastic' && !isDrastic(name, args))) return next(e)
    const server = /^mcp__(.+?)__/.exec(e.tool)![1]
    const title =
      name === 'save_document' && typeof args.id === 'string' ? await documentTitle($, server, args.id) : undefined
    if (title) args = { ...args, id: `"${title}"` }
    const warning = isDrastic(name, args) ? ' Everyone on the team sees this.' : ''
    return { decision: 'ask', reason: `${$.plugin.name}: ${actionOf(name, args)}.${warning}` }
  }).catch(($, e) => ({ decision: 'deny', reason: `${$.plugin.name}: could not describe this Linear write, so it is refused.` }))
}
