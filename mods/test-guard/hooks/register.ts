import { atom, read, update } from 'claude-code'
import type { Hook, Register, SessionRepo } from 'claude-code'
import { align, apply, findings, kindOf, lostLines, maybeGuarded, minus, nameKind } from './check'
import type { Change, Finding, Kind } from './check'
import type { Approved, Call, Mode, Profile, Turn } from '../types'

type Api = Parameters<Hook<'tool.call'>>[0]

const MOD = 'test-guard'
const TOOLS = new Set(['Edit', 'MultiEdit', 'Write'])
const NO_BASELINE = [/not a git repository/, /invalid object name '?HEAD'?/, /does not exist in '?HEAD'?/, /exists on disk, but not in '?HEAD'?/]
const USAGE = 'Use /test-guard allow <path> to let Claude change the lines that path has at HEAD, or /test-guard to list allowed paths.'
// The origins where the user typed the command. A model, a peer session or a coordinator never grants a path.
const USER = new Set(['composer', 'bridge', 'sdk'])
// /test-guard setup replays at most this many commits, and stops at CAP guarded file changes.
const COMMITS = 200
const CAP = 300
const MODES: readonly Mode[] = ['rigs', 'full', 'off']
// What the small model reads to pick the rules: the rule sets and the replay counts, never text from the repository.
const BRIEF = 'test-guard stops a coding agent from passing a failing test by weakening the test. ' +
  'Each rule that fires on an edit asks a person to approve it. Pick the rules for one repository from its history. ' +
  'rigs: the content rules only (an added skip, exit, report patch, always-true equality or pass-anyway flag); few honest edits trip them. ' +
  'full: the rig rules, plus an ask on any change to a line a test or runner file has at HEAD. ' +
  'off: no rules. ' +
  'Pick full when it would ask about few of the changes, rigs when full would ask about many, off only when even the rig rules would ask about most.'
const NAMED: Record<Mode, string> = { rigs: 'rig rules only', full: 'full rules', off: 'off' }
const CHOOSE = 'Run `/test-guard setup rigs`, `/test-guard setup full` or `/test-guard setup off` to choose.'

const allowed = atom({ plugin: 'test-guard', key: 'allowed' } as const, [] as string[])
const turn = atom({ plugin: 'test-guard', key: 'turn' } as const, null as Turn | null)
const noted = atom({ plugin: 'test-guard', key: 'noted' } as const, [] as string[])
// What tool.check said about a call, by tool_use_id, until its tool.call reads it.
const calls = atom({ plugin: 'test-guard', key: 'calls' } as const, {} as Record<string, Call>)
const approved = atom({ plugin: 'test-guard', key: 'approved' } as const, {} as Approved)
// Paths whose HEAD lines a person approved changing, until the turn ends.
const opened = atom({ plugin: 'test-guard', key: 'opened' } as const, [] as string[])

// The person reads `ask` in the approval dialog; the model reads `deny` and `failed`.
const ask = (f: Finding) =>
  `${MOD}: this edit ${f.what}: \`${f.line.trim()}\`. ` +
  (f.lost ? 'Approve to let Claude change existing lines in this file until the turn ends.' : 'Approve it if you asked for this change.')
const deny = (path: string, f: Finding) =>
  `${MOD}: this edit ${f.what}: \`${f.line.trim()}\`, and nobody is here to approve it. ` +
  `Finish the task without this change, then stop and tell the user which test, the old line and why, so they can run \`/test-guard allow ${path}\`.`
const failed = (why: string) =>
  `${MOD}: could not check this edit (${why}). Retry once; if it fails again, stop and tell the user, who can run \`/test-guard allow <path>\`.`

function absolute(path: string, cwd: string): string {
  const parts: string[] = []
  for (const s of (path.startsWith('/') ? path : `${cwd}/${path}`).split('/')) {
    if (s === '..') parts.pop()
    else if (s && s !== '.') parts.push(s)
  }
  return `/${parts.join('/')}`
}

async function after($: Api, tool: string, e: Record<string, unknown>, path: string): Promise<string> {
  if (tool === 'Write') return String(e.content)
  const changes = tool === 'MultiEdit' ? (e.edits as Change[]) : [e as unknown as Change]
  return changes.reduce(apply, String(await $.fs.read(path)))
}

async function nearestDir($: Api, path: string): Promise<{ dir: string; rel: string }> {
  let dir = path.slice(0, path.lastIndexOf('/')) || '/'
  while (dir !== '/' && !(await $.fs.exists(dir))) dir = dir.slice(0, dir.lastIndexOf('/')) || '/'
  return { dir, rel: path.slice(dir === '/' ? 1 : dir.length + 1) }
}

async function kind($: Api, path: string): Promise<Kind | undefined> {
  const named = nameKind(path)
  if (named) return named
  const { dir, rel } = await nearestDir($, path)
  // --show-prefix, not --show-toplevel: toplevel resolves symlinks (/tmp -> /private/tmp) and breaks the prefix cut.
  const r = await $.process.run(['git', 'rev-parse', '--show-prefix'], { cwd: dir })
  if (r.exitCode === 0) return kindOf(`${r.stdout.trim()}${rel.replace(/\\/g, '/')}`)
  if (NO_BASELINE.some(re => re.test(r.stderr))) return undefined
  throw new Error(`git rev-parse exited ${r.exitCode}: ${r.stderr.trim()}`)
}

async function headText($: Api, path: string): Promise<string | undefined> {
  const { dir, rel } = await nearestDir($, path)
  const r = await $.process.run(['git', 'show', `HEAD:./${rel}`], { cwd: dir })
  if (r.exitCode === 0) return r.stdout
  if (NO_BASELINE.some(re => re.test(r.stderr))) return undefined
  throw new Error(`git show exited ${r.exitCode}: ${r.stderr.trim()}`)
}

// The repo root and HEAD commit seen from the session's folder, or undefined outside a repo with a commit.
async function base($: Api): Promise<{ root: string; sha: string } | undefined> {
  const cwd = await $.session.cwd()
  const r = await $.process.run(['git', 'rev-parse', '--show-cdup', 'HEAD'], { cwd })
  if (r.exitCode !== 0) return undefined
  const [cdup = '', sha = ''] = r.stdout.split('\n')
  return sha.trim() ? { root: absolute(cdup || '.', cwd), sha: sha.trim() } : undefined
}

// The first lost line of each guarded tracked file that differs from `sha`, deleted files included.
async function losses($: Api, root: string, sha: string): Promise<Map<string, string>> {
  const out = new Map<string, string>()
  const d = await $.process.run(['git', 'diff', '--name-only', '--no-renames', '-z', sha, '--'], { cwd: root })
  if (d.exitCode !== 0) throw new Error(`git diff exited ${d.exitCode}`)
  const ok = await read($, allowed)
  const yes = await read($, approved)
  const open = await read($, opened)
  for (const rel of d.stdout.split('\0').filter(Boolean)) {
    const k = kindOf(rel)
    const path = `${root}/${rel}`
    if ((k !== 'test' && k !== 'config') || ok.includes(path) || open.includes(path)) continue
    const head = await $.process.run(['git', 'show', `${sha}:${rel}`], { cwd: root })
    if (head.exitCode !== 0) continue
    const now = (await $.fs.exists(path)) ? String(await $.fs.read(path)) : ''
    const lost = minus(align(head.stdout, now, rel).gone, yes[path])[0]
    if (lost !== undefined) out.set(path, lost)
  }
  return out
}

// A repository's profile is keyed by its origin remote, else its main working tree, so every worktree shares it.
const profileKey = (repo: SessionRepo) => `profile:${repo.remote ?? repo.root}`
const repoName = (repo: SessionRepo) => repo.name ?? repo.root.slice(repo.root.lastIndexOf('/') + 1)

async function profile($: Api): Promise<{ repo: SessionRepo; profile?: Profile } | null> {
  const repo = await $.session.repo()
  if (!repo) return null
  return { repo, profile: (await $.store.get(profileKey(repo))) as Profile | undefined }
}

// The rules for the session's repository: off with no profile, outside a repo, or when the store fails.
async function mode($: Api): Promise<Mode> {
  try {
    const m = (await profile($))?.profile?.mode
    return m === 'rigs' || m === 'full' ? m : 'off'
  } catch (cause) {
    $.ui.log(`${MOD}: could not read this project's profile (${String(cause)}); the guard is off for this call.`, { to: 'debug' })
    return 'off'
  }
}

type Replay = { commits: number; changes: number; full: number; rigs: number; capped: boolean }

// Runs the project's own recent history through the rules: how many guarded file changes each rule set would ask about.
async function replay($: Api, root: string): Promise<Replay> {
  const out: Replay = { commits: 0, changes: 0, full: 0, rigs: 0, capped: false }
  const log = await $.process.run(['git', 'log', '--no-merges', `-n${COMMITS}`, '--no-renames', '--name-status', '-z', '--format=%x01%H %P'], { cwd: root })
  if (log.exitCode !== 0) {
    if (/does not have any commits yet/.test(log.stderr)) return out
    throw new Error(`git log exited ${log.exitCode}: ${log.stderr.trim()}`)
  }
  const show = async (spec: string) => {
    const r = await $.process.run(['git', 'show', spec], { cwd: root })
    return r.exitCode === 0 ? r.stdout : undefined
  }
  for (const record of log.stdout.split('\x01').slice(1)) {
    const [header = '', ...files] = record.split('\0')
    const [sha, parent] = header.trim().split(' ')
    out.commits++
    if (!sha || !parent) continue
    for (let i = 0; i + 1 < files.length; i += 2) {
      const status = (files[i] as string).trim()
      const rel = files[i + 1] as string
      const k = kindOf(rel)
      if ((status !== 'M' && status !== 'D') || (k !== 'test' && k !== 'config')) continue
      if (out.changes === CAP) return { ...out, capped: true }
      const head = await show(`${sha}^:${rel}`)
      const text = status === 'D' ? '' : await show(`${sha}:${rel}`)
      if (head === undefined || text === undefined) continue
      out.changes++
      if (findings(k, rel, head, text)) out.full++
      if (findings(k, rel, head, text, true)) out.rigs++
    }
  }
  return out
}

function replayed(name: string, r: Replay): string {
  if (r.commits < 2 && !r.capped) return `In ${name}, the history has fewer than 2 commits to learn from.`
  const last = `the last ${r.commits} commit${r.commits === 1 ? '' : 's'}${r.capped ? ` (cut at ${CAP} file changes)` : ''}`
  if (!r.changes) return `In ${name}, ${last} changed no test or runner file.`
  return `In ${name}, ${last} made ${r.changes} changes to test or runner files; ` +
    `the full rules would have asked you about ${r.full} of them and the rig rules about ${r.rigs}.`
}

// With no choice, a small model picks the mode from the replay counts. The session's own model never picks.
async function setup($: Api, choice: Mode | undefined): Promise<string> {
  const repo = await $.session.repo()
  if (!repo) return 'Not in a git repository.'
  const name = repoName(repo)
  const r = await replay($, repo.root)
  let m = choice
  if (m === undefined) {
    let label: string | undefined
    try {
      label = await $.model.classify(`${BRIEF}\n\n${replayed(name, r)}`, MODES, { model: 'haiku' })
    } catch (cause) {
      $.ui.log(`${MOD}: the model could not pick the rules (${String(cause)}).`, { to: 'debug' })
    }
    m = MODES.find(x => x === label)
    if (!m) return `${MOD}: nothing saved, since the model picked no rules. ${replayed(name, r)} ${CHOOSE}`
  }
  const saved: Profile = { mode: m, by: choice ? 'user' : 'model', at: new Date(await $.clock.now()).toISOString(), commits: r.commits, changes: r.changes, full: r.full, rigs: r.rigs }
  await $.store.set(profileKey(repo), saved)
  const why = choice ? '' : ` ${replayed(name, r)}`
  return `${MOD}: ${NAMED[m]} in ${name}, ${choice ? 'as you chose' : 'picked by the model'}.${why} Run \`/test-guard setup rigs\`, \`full\` or \`off\` to change it.`
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await $.command.register({
      name: 'test-guard',
      description: 'Show or change the rules test-guard runs in this project, or let Claude change the HEAD lines of one test file',
      argumentHint: 'setup [rigs|full|off] | allow <path>',
    })
    try {
      const p = await profile($)
      if (p && !p.profile) $.ui.toast(await setup($, undefined))
    } catch (cause) {
      $.ui.log(`${MOD}: could not set up this project (${String(cause)}).`, { to: 'debug' })
    }
    return result
  })

  on('command.run', { command: 'test-guard' }, async ($, e) => {
    const [verb, ...rest] = e.args.trim().split(/\s+/)
    const user = !e.origin || USER.has(e.origin.kind)
    if (!verb) {
      const p = await profile($)
      const set = p?.profile
        ? `Rules: ${NAMED[p.profile.mode]} in this project, set ${p.profile.at.slice(0, 10)}${p.profile.by ? ` by ${p.profile.by === 'user' ? 'you' : 'the model'}` : ''}.`
        : 'Not set up in this project; run /test-guard setup.'
      const paths = await read($, allowed)
      return { text: `${set}\n${paths.length ? `Allowed: ${paths.join(', ')}` : `No path is allowed. ${USAGE}`}` }
    }
    if (verb === 'setup' && rest.length <= 1 && (!rest[0] || rest[0] in NAMED)) {
      if (!user) return { text: 'Only the user can set up test-guard, by typing /test-guard setup at the prompt.' }
      return { text: await setup($, rest[0] as Mode | undefined) }
    }
    if (verb !== 'allow' || !rest.length) return { text: USAGE }
    if (!user) return { text: `${MOD}: only the user can allow a path, by typing /test-guard allow at the prompt.` }
    const path = absolute(rest.join(' '), await $.session.cwd())
    await update($, allowed, paths => (paths.includes(path) ? paths : [...paths, path]))
    return { text: `Claude can now change the HEAD lines of ${path} for the rest of this session.` }
  })

  // The gate: a finding goes to the person present, and is refused where nobody can be asked.
  // It only tightens the verdict beneath, and records its answer for the call's tool.call.
  on('tool.check', async ($, e, next) => {
    const r = await next(e)
    if (r.decision === 'deny' || !TOOLS.has(e.tool)) return r
    const input = (e.input ?? {}) as Record<string, unknown>
    if (typeof input.file_path !== 'string' || !maybeGuarded(input.file_path)) return r
    // Every throw below has a profile of rigs or full behind it, so the catch fails closed.
    const m = await mode($)
    if (m === 'off') return r
    const path = absolute(input.file_path, await $.session.cwd())
    const k = await kind($, path)
    if (!k || (await read($, allowed)).includes(path)) return r
    const head = await headText($, path)
    const text = await after($, e.tool, input, path)
    // In rigs mode the HEAD-line rule never runs, as for an opened path.
    const open = m === 'rigs' || (await read($, opened)).includes(path)
    const before = head !== undefined && (await $.fs.exists(path)) ? String(await $.fs.read(path)) : ''
    const f = findings(k, path, head, text, open, head === undefined ? [] : lostLines(head, before, path))
    const lost = head === undefined ? [] : lostLines(head, text, path)
    // An edit to an opened path runs with no ask; its lost lines are recorded as approved too.
    let call: Call | undefined = open && lost.length ? { path, lost } : undefined
    if (f) call = e.approver ? { path, lost, ...(f.lost ? { opens: true as const } : {}) } : { deny: deny(path, f) }
    if (call && e.tool_use_id) await update($, calls, m => ({ ...m, [e.tool_use_id as string]: call }))
    if (!f) return r
    return call && 'deny' in call ? { decision: 'deny', reason: call.deny } : { decision: 'ask', reason: ask(f) }
  }).catch(async ($, e, next) => {
    const reason = failed(next.error.message)
    try {
      if (e.tool_use_id) await update($, calls, m => ({ ...m, [e.tool_use_id as string]: { deny: reason } }))
    } catch {}
    return { decision: 'deny', reason }
  })

  // tool.check runs inside this call's next(e). A refusal there comes back as the mod's own deny; an
  // approved edit that ran records the HEAD lines it lost, so the turn-end check leaves them out.
  on('tool.call', async ($, e, next) => {
    if (!TOOLS.has(e.tool)) return next(e)
    const r = await next(e)
    const id = e.tool_use_id
    const c = (await read($, calls))[id]
    if (!c) return r
    await update($, calls, ({ [id]: _, ...rest }) => rest)
    if ('deny' in c) return { deny: c.deny }
    if (r.deny !== undefined || (r as { isError?: boolean }).isError) return r
    if (c.opens) await update($, opened, o => (o.includes(c.path) ? o : [...o, c.path]))
    if (c.lost.length)
      await update($, approved, a => {
        const had = { ...a[c.path] }
        for (const l of c.lost) had[l] = Math.max(had[l] ?? 0, c.lost.filter(x => x === l).length)
        return { ...a, [c.path]: had }
      })
    return r
  }).catch(($, e, next) => (next.called ? next(e) : { deny: failed(next.error.message) }))

  // Claude Code owns Bash, so a `sed -i`, `rm` or `jest -u` on a test runs. At the turn's start the
  // hook notes HEAD and the losses already there; at the turn's end it compares the guarded tracked
  // files with that HEAD and blocks the stop once for each new loss, so Claude puts the line back or
  // tells the user. It never denies a tool call.
  on('turn.start', async ($, e, next) => {
    const result = await next(e)
    if (e.agentId !== undefined) return result
    if ((await mode($)) !== 'full') {
      await update($, turn, () => null)
      return result
    }
    // A refused ask never reaches its tool.call, so its id is left here; an approval opens a path for one turn.
    await update($, calls, () => ({}))
    await update($, opened, () => [])
    try {
      const b = await base($)
      const had = b ? [...(await losses($, b.root, b.sha))] : []
      await update($, turn, () => (b ? { ...b, had } : null))
    } catch (cause) {
      await update($, turn, () => null)
      $.ui.log(`${MOD}: could not read HEAD at the turn's start (${String(cause)}); this turn's Bash changes are not checked.`, { to: 'debug' })
    }
    return result
  })

  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    if (result.block !== undefined || result.preventContinuation) return result
    const t = await read($, turn)
    if (!t || (await mode($)) !== 'full') return result
    try {
      // A commit in the turn keeps the turn's HEAD as the base; a checkout or a reset takes the new one.
      let sha = t.sha
      const now = await base($)
      if (now && now.sha !== sha) {
        const anc = await $.process.run(['git', 'merge-base', '--is-ancestor', sha, now.sha], { cwd: t.root })
        if (anc.exitCode !== 0) sha = now.sha
      }
      const had = new Map(t.had)
      const seen = await read($, noted)
      const fresh = [...(await losses($, t.root, sha))].filter(([p, l]) => had.get(p) !== l && !seen.includes(`${p}\n${l}`))
      if (!fresh.length) return result
      await update($, noted, n => [...n, ...fresh.map(([p, l]) => `${p}\n${l}`)])
      $.ui.log(`${MOD}: this turn changed or removed HEAD lines of ${fresh.map(([p]) => p).join(', ')} outside Edit and Write.`)
      const list = fresh.map(([p, l]) => `${p}: \`${l.trim()}\``).join('; ')
      return {
        ...result,
        block: `${MOD}: this turn changed or removed a line that a test or runner config has at HEAD, outside Edit and Write: ${list}. ` +
          'If the user did not ask for it, put the line back; if the test is wrong, stop and tell the user which test, the old line and why.',
      }
    } catch (cause) {
      $.ui.log(`${MOD}: could not compare the test files with HEAD (${String(cause)}).`, { to: 'debug' })
      return result
    }
  })
}
