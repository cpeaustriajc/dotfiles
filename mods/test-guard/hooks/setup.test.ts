import { expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

// A project for the profile and /test-guard setup: `history` is oldest first, a null file is a delete.
type Commit = { sha: string; files: Record<string, string | null> }
type Project = {
  root: string
  cwd: string
  remote: string | null
  inRepo: boolean
  store: Record<string, unknown>
  storeFails: boolean
  history: Commit[]
  disk: Record<string, string>
  pick: string | Error | undefined
  picked: { text: string; labels: readonly string[]; model?: string }[]
  sets: { key: string; value: unknown }[]
  toasts: string[]
  logs: string[]
  ran: unknown[]
}

const T = 'tests/a.test.ts'
const T_HEAD = "it('sends once', () => {\n  expect(send).toHaveBeenCalledTimes(1)\n})\n"
const P = 'tests/test_b.py'
const P_HEAD = 'def test_b():\n    assert b() == 1\n'
const NOW = Date.UTC(2026, 10, 13, 9, 30)

function project(on: On, given: Partial<Project> = {}): Project {
  const w: Project = {
    root: '/repo', cwd: '/repo', remote: null, inRepo: true, store: {}, storeFails: false,
    history: [{ sha: 'c1', files: { [T]: T_HEAD, [P]: P_HEAD } }], disk: { [T]: T_HEAD, [P]: P_HEAD },
    pick: 'rigs', picked: [], sets: [], toasts: [], logs: [], ran: [], ...given,
  }
  const snap = (i: number) => {
    const files: Record<string, string> = {}
    for (const c of w.history.slice(0, i + 1)) for (const [p, t] of Object.entries(c.files)) t === null ? delete files[p] : (files[p] = t)
    return files
  }
  const at = (sha: string) => snap(w.history.findIndex(c => c.sha === sha))
  const ok = (stdout: string) => ({ value: { exitCode: 0, stdout, stderr: '' } }) as never
  const fail = (stderr: string) => ({ value: { exitCode: 128, stdout: '', stderr } }) as never
  const rel = (p: string) => p.slice(w.cwd.length + 1)
  mock.clock(on, { now: NOW })
  on('session.cwd', () => ({ value: w.cwd }) as never)
  on('session.repo', () => ({ value: w.inRepo ? { root: w.root, remote: w.remote, internal: false, name: null } : null }) as never)
  on('store.get', (_$, e) => {
    if (w.storeFails) throw new Error('store: disk full')
    return { value: w.store[(e as { key: string }).key] } as never
  })
  on('store.set', (_$, e) => {
    const { key, value } = e as { key: string; value: unknown }
    w.sets.push({ key, value })
    w.store[key] = value
    return { value: undefined } as never
  })
  on('ui.toast', (_$, e) => (w.toasts.push((e as { text: string }).text), { value: undefined }) as never)
  on('ui.log', (_$, e) => (w.logs.push((e as { text: string }).text), { value: undefined }) as never)
  on('fs.exists', (_$, e) => {
    const p = rel((e as { path: string }).path)
    return { value: p in w.disk || Object.keys(w.disk).some(f => f.startsWith(`${p}/`)) || (e as { path: string }).path === w.cwd } as never
  })
  on('fs.read', (_$, e) => ({ value: w.disk[rel((e as { path: string }).path)] }) as never)
  on('process.run', (_$, e) => {
    const { argv, init } = e as { argv: string[]; init?: { cwd?: string } }
    if (!w.inRepo) return fail('fatal: not a git repository')
    const [, verb, ...rest] = argv
    const head = w.history[w.history.length - 1]!.sha
    if (verb === 'rev-parse') return ok(argv.includes('HEAD') ? `\n${head}\n` : '')
    if (verb === 'log') {
      const out = w.history.slice().reverse().map(c => {
        const i = w.history.indexOf(c)
        const before = i ? snap(i - 1) : {}
        const files = Object.entries(c.files).map(([p, t]) => `${t === null ? 'D' : p in before ? 'M' : 'A'}\0${p}\0`).join('')
        return `\x01${c.sha} ${i ? w.history[i - 1]!.sha : ''}\0\n${files}`
      })
      return ok(out.join(''))
    }
    if (verb === 'diff') {
      const base = at(rest[3] as string)
      return ok(Object.keys(base).filter(p => base[p] !== w.disk[p]).map(p => `${p}\0`).join(''))
    }
    if (verb === 'show') {
      const spec = rest[0] as string
      const [rev, path] = spec.startsWith('HEAD:./') ? [head, `${rel(init?.cwd ?? w.cwd) ? `${rel(init?.cwd ?? w.cwd)}/` : ''}${spec.slice(7)}`] : spec.split(':') as [string, string]
      const sha = rev.endsWith('^') ? w.history[w.history.findIndex(c => c.sha === rev.slice(0, -1)) - 1]?.sha : rev
      const text = sha ? at(sha)[path] : undefined
      return text === undefined ? fail(`fatal: path '${path}' does not exist in '${rev}'`) : ok(text)
    }
    return fail(`unexpected ${argv.join(' ')}`)
  })
  on('tool.call', (_$, e) => (w.ran.push(e), { result: { ok: true } }) as never)
  on('model.classify', (_$, e) => {
    const c = e as { text: string; labels: readonly string[]; options?: { model?: string } }
    w.picked.push({ text: c.text, labels: c.labels, model: c.options?.model })
    if (w.pick instanceof Error) throw w.pick
    return { value: w.pick } as never
  })
  on('tool.check', () => ({ decision: 'allow', reason: 'core' }) as never)
  on('command.register', () => ({ value: {} }) as never)
  on('session.start', (_$, e) => e as never)
  on('turn.start', (_$, e) => ({ turnId: (e as { turnId: string }).turnId }) as never)
  on('classic.Stop', () => ({}) as never)
  return w
}

const profileOf = (mode: string) => ({ mode, at: '2026-11-01T08:00:00.000Z', commits: 6, changes: 4, full: 3, rigs: 1 })
const run = ($: any, args: string, kind = 'composer') => $.command.run({ command: 'test-guard', args, origin: { kind } })
const check = ($: any, input: Record<string, unknown>, approver?: 'person') =>
  $.tool.check({ tool: 'Edit', input, tool_use_id: 'u1', ...(approver ? { approver } : {}) })
const WEAKEN = { file_path: `/repo/${T}`, old_string: 'toHaveBeenCalledTimes(1)', new_string: 'toHaveBeenCalled()' }
const EXIT = { file_path: `/repo/${P}`, old_string: '    assert b() == 1\n', new_string: `    assert b() == 1\nimport sys\nsys.${'exit'}(0)\n` }
const SKIP = { file_path: `/repo/${P}`, old_string: 'def test_b', new_string: '@pytest.mark.skip\ndef test_b' }
const start = ($: any) => $.turn.start({ text: 'go', turnId: 't1' })
const stop = async ($: any) => (await $.classic.Stop({ session_id: 's', transcript_path: '/t', stop_hook_active: false })).block as string | undefined

for (const [name, store] of [['no profile', {}], ['an off profile', { 'profile:/repo': profileOf('off') }]] as const) {
  test(`${name}: a changed HEAD line and an added exit get the verdict beneath, with and without an approver`, async ($, on) => {
    project(on, { store })
    for (const input of [WEAKEN, EXIT])
      for (const approver of ['person', undefined] as const) {
        const r = await check($, input, approver)
        expect(r.decision).toBe('allow')
        expect(r.reason).toBe('core')
      }
  })

  test(`${name}: tool.call passes, and a loss through Bash does not block the stop`, async ($, on) => {
    const w = project(on, { store })
    expect((await ($ as any).tool.call({ tool: 'Edit', ...WEAKEN })).deny).toBeUndefined()
    expect(w.ran.length).toBe(1)
    await start($)
    w.disk[T] = ''
    expect(await stop($)).toBeUndefined()
  })
}

test('rigs: a changed HEAD line passes with no ask, a skip on a HEAD test is asked or denied, a Bash loss passes the stop', async ($, on) => {
  const w = project(on, { store: { 'profile:/repo': profileOf('rigs') } })
  for (const approver of ['person', undefined] as const) expect((await check($, WEAKEN, approver)).decision).toBe('allow')
  expect((await check($, SKIP, 'person')).decision).toBe('ask')
  expect((await check($, SKIP)).decision).toBe('deny')
  await start($)
  w.disk[T] = ''
  expect(await stop($)).toBeUndefined()
})

test('full: a changed HEAD line is still asked', async ($, on) => {
  project(on, { store: { 'profile:/repo': profileOf('full') } })
  expect((await check($, WEAKEN, 'person')).decision).toBe('ask')
})

test('the profile is found by the remote when the repo has one, else by the root, and from a worktree', async ($, on) => {
  const remote = 'git@github.com:o/r.git'
  const w = project(on, { remote, store: { [`profile:${remote}`]: profileOf('full'), 'profile:/repo': profileOf('off') } })
  expect((await check($, WEAKEN, 'person')).decision).toBe('ask')
  w.remote = null
  expect((await check($, WEAKEN, 'person')).decision).toBe('allow')
  w.store['profile:/repo'] = profileOf('full')
  w.cwd = '/repo-wt'
  expect((await check($, { ...WEAKEN, file_path: `/repo-wt/${T}` }, 'person')).decision).toBe('ask')
  w.remote = remote
  w.store['profile:/repo'] = profileOf('off')
  expect((await check($, { ...WEAKEN, file_path: `/repo-wt/${T}` }, 'person')).decision).toBe('ask')
})

test('a store read error during tool.check passes the call through', async ($, on) => {
  const w = project(on, { storeFails: true })
  const r = await check($, WEAKEN)
  expect(r.decision).toBe('allow')
  expect(r.reason).toBe('core')
  expect(w.logs.some(l => l.includes("could not read this project's profile"))).toBe(true)
})

// Root c0, then an honest value change, an added test, an added skip marker, a deleted test file, a new test file.
const C = 'tests/c.test.ts'
const HISTORY: Commit[] = [
  { sha: 'c0', files: { [T]: T_HEAD, [P]: P_HEAD, [C]: "it('c', () => {\n  expect(c).toBe(1)\n})\n", 'src/a.ts': 'a\n' } },
  { sha: 'c1', files: { [T]: T_HEAD.replace('Times(1)', 'Times(2)'), 'src/a.ts': 'b\n' } },
  { sha: 'c2', files: { [T]: `${T_HEAD.replace('Times(1)', 'Times(2)')}it('more', () => {})\n` } },
  { sha: 'c3', files: { [P]: `@pytest.mark.skip\n${P_HEAD}` } },
  { sha: 'c4', files: { [C]: null } },
  { sha: 'c5', files: { 'tests/d.test.ts': "it('d', () => {})\n" } },
]
const NUMBERS = 'In repo, the last 6 commits made 4 changes to test or runner files; the full rules would have asked you about 3 of them and the rig rules about 1.'

const CHANGE = 'Run `/test-guard setup rigs`, `full` or `off` to change it.'

test('setup: the model picks from the replay counts alone, and the profile records it', async ($, on) => {
  const w = project(on, { history: HISTORY })
  const out = await run($, 'setup')
  expect(w.picked.length).toBe(1)
  expect(w.picked[0]!.labels).toEqual(['rigs', 'full', 'off'])
  expect(w.picked[0]!.model).toBe('haiku')
  expect(w.picked[0]!.text.endsWith(`\n\n${NUMBERS}`)).toBe(true)
  expect(w.picked[0]!.text).not.toContain('pytest.mark.skip')
  expect(w.sets).toEqual([{ key: 'profile:/repo', value: { mode: 'rigs', by: 'model', at: '2026-11-13T09:30:00.000Z', commits: 6, changes: 4, full: 3, rigs: 1 } }])
  expect(out.text).toBe(`test-guard: rig rules only in repo, picked by the model. ${NUMBERS} ${CHANGE}`)
})

test('setup: each label the model names saves its mode', async ($, on) => {
  const w = project(on, { history: HISTORY })
  for (const mode of ['rigs', 'full', 'off']) {
    w.pick = mode
    await run($, 'setup')
    expect((w.store['profile:/repo'] as { mode: string }).mode).toBe(mode)
  }
})

test('setup: no label, or a failed call, saves nothing and names the three commands', async ($, on) => {
  const w = project(on, { history: HISTORY })
  for (const pick of [undefined, new Error('api-error 529')]) {
    w.pick = pick
    const out = await run($, 'setup')
    expect(out.text).toBe(`test-guard: nothing saved, since the model picked no rules. ${NUMBERS} Run \`/test-guard setup rigs\`, \`/test-guard setup full\` or \`/test-guard setup off\` to choose.`)
  }
  expect(w.sets).toEqual([])
  expect(w.logs.some(l => l.includes('the model could not pick the rules'))).toBe(true)
})

test('setup rigs saves with the replay numbers and no model call', async ($, on) => {
  const w = project(on, { history: HISTORY })
  expect((await run($, 'setup rigs')).text).toBe(`test-guard: rig rules only in repo, as you chose. ${CHANGE}`)
  expect(w.picked).toEqual([])
  expect(w.sets).toEqual([{ key: 'profile:/repo', value: { mode: 'rigs', by: 'user', at: '2026-11-13T09:30:00.000Z', commits: 6, changes: 4, full: 3, rigs: 1 } }])
})

test('setup from an origin other than the user saves nothing and calls no model', async ($, on) => {
  const w = project(on, { history: HISTORY, pick: 'off' })
  for (const kind of ['peer-send-message', 'coordinator', 'plugin', 'unclassified'])
    for (const args of ['setup', 'setup off']) expect((await run($, args, kind)).text).toContain('Only the user can set up')
  expect(w.picked).toEqual([])
  expect(w.sets).toEqual([])
})

test('setup stops the replay at 300 file changes and tells the model so', async ($, on) => {
  const files = Object.fromEntries(Array.from({ length: 301 }, (_, i) => [`tests/t${i}.test.ts`, 'a\n']))
  const changed = Object.fromEntries(Object.keys(files).map(p => [p, 'b\n']))
  const w = project(on, { history: [{ sha: 'c0', files }, { sha: 'c1', files: changed }] })
  await run($, 'setup')
  expect(w.picked[0]!.text).toContain('the last 1 commit (cut at 300 file changes) made 300 changes to test or runner files; the full rules would have asked you about 300')
})

test('setup still picks in a repo with one commit, or with no test change, and says so', async ($, on) => {
  const w = project(on)
  await run($, 'setup')
  expect(w.picked[0]!.text.endsWith('In repo, the history has fewer than 2 commits to learn from.')).toBe(true)
  w.history = [HISTORY[0]!, { sha: 'c1', files: { 'src/a.ts': 'b\n' } }]
  await run($, 'setup')
  expect(w.picked[1]!.text.endsWith('In repo, the last 2 commits changed no test or runner file.')).toBe(true)
})

test('/test-guard alone shows the mode and the date, or not set up', async ($, on) => {
  const w = project(on)
  expect((await run($, '')).text).toBe('Not set up in this project; run /test-guard setup.\nNo path is allowed. Use /test-guard allow <path> to let Claude change the lines that path has at HEAD, or /test-guard to list allowed paths.')
  w.store['profile:/repo'] = profileOf('rigs')
  expect((await run($, '')).text).toContain('Rules: rig rules only in this project, set 2026-11-01.\n')
  w.store['profile:/repo'] = { ...profileOf('full'), by: 'model' }
  expect((await run($, '')).text).toContain('Rules: full rules in this project, set 2026-11-01 by the model.\n')
})

test('session.start: with no profile the model picks and a toast says so; nothing with a profile, outside a repo, or when the store fails', async ($, on) => {
  const w = project(on, { history: HISTORY })
  const begin = () => ($ as any).session.start({ cwd: '/repo', isInteractive: true })
  await begin()
  expect(w.toasts).toEqual([`test-guard: rig rules only in repo, picked by the model. ${NUMBERS} ${CHANGE}`])
  expect((w.store['profile:/repo'] as { by: string }).by).toBe('model')
  await begin()
  w.store = {}
  w.inRepo = false
  await begin()
  w.inRepo = true
  w.storeFails = true
  await begin()
  expect(w.toasts.length).toBe(1)
  expect(w.picked.length).toBe(1)
  expect(w.logs.some(l => l.includes('could not set up this project'))).toBe(true)
})

test('session.start: a failed pick saves nothing, toasts the three commands and picks again next session', async ($, on) => {
  const w = project(on, { history: HISTORY, pick: new Error('api-error 529') })
  await ($ as any).session.start({ cwd: '/repo', isInteractive: true })
  expect(w.sets).toEqual([])
  expect(w.toasts[0]).toContain('nothing saved, since the model picked no rules')
  w.pick = 'full'
  await ($ as any).session.start({ cwd: '/repo', isInteractive: true })
  expect((w.store['profile:/repo'] as { mode: string }).mode).toBe('full')
})
