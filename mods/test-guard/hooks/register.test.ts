import { expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

type World = {
  ran: unknown[]
  commands: string[]
  runs: { argv: string[]; cwd?: string }[]
  disk: Record<string, string>
  head: Record<string, string>
  repo: 'yes' | 'no' | 'unborn' | 'broken' | 'throws'
  root: string
  // This repository's test-guard profile; the full rules unless a test gives another, or null for none.
  profile?: { mode: string; at: string } | null
}

const A = '/repo/tests/a.test.ts'
const A_HEAD = [
  "import { notify } from '../src/notify'",
  '',
  "it('sends once', () => {",
  '  notify()',
  '  expect(send).toHaveBeenCalledTimes(1)',
  "  expect(send).toHaveBeenCalledWith('hi')",
  '})',
  '',
].join('\n')

function world(on: On, given: Partial<World> = {}): World {
  const w: World = { ran: [], commands: [], runs: [], disk: { [A]: A_HEAD }, head: { [A]: A_HEAD }, repo: 'yes', root: '/repo', ...given }
  const profile = 'profile' in given ? given.profile : { mode: 'full', at: '2026-11-13T00:00:00.000Z', commits: 0, changes: 0, full: 0, rigs: 0 }
  on('session.repo', () => ({ value: { root: w.root, remote: null, internal: false, name: null } }) as never)
  on('store.get', (_$, e) => ({ value: (e as { key: string }).key === `profile:${w.root}` && profile ? profile : undefined }) as never)
  const isDir = (p: string) => p === w.root || Object.keys(w.disk).some(f => f.startsWith(`${p}/`))
  on('session.cwd', () => ({ value: '/repo' }) as never)
  on('fs.exists', (_$, e) => {
    const p = (e as { path: string }).path
    return { value: p in w.disk || isDir(p) } as never
  })
  on('fs.read', (_$, e) => {
    const p = (e as { path: string }).path
    if (!(p in w.disk)) throw new Error(`ENOENT: ${p}`)
    return { value: w.disk[p] } as never
  })
  on('process.run', (_$, e) => {
    const { argv, init } = e as { argv: string[]; init?: { cwd?: string } }
    w.runs.push({ argv, cwd: init?.cwd })
    const fail = (stderr: string) => ({ value: { exitCode: 128, stdout: '', stderr } }) as never
    if (w.repo === 'throws') throw new Error('git: not found')
    if (w.repo === 'no') return fail('fatal: not a git repository (or any of the parent directories): .git')
    if (w.repo === 'unborn') return fail("fatal: invalid object name 'HEAD'.")
    if (w.repo === 'broken') return fail('fatal: unable to read tree 1234abcd')
    if (argv[1] === 'rev-parse') {
      const prefix = init?.cwd === w.root ? '' : `${init?.cwd?.slice(w.root.length + 1)}/`
      return { value: { exitCode: 0, stdout: `${prefix}\n`, stderr: '' } } as never
    }
    const abs = `${init?.cwd}/${argv[argv.length - 1].replace(/^HEAD:\.\//, '')}`
    if (abs in w.head) return { value: { exitCode: 0, stdout: w.head[abs], stderr: '' } } as never
    return fail(`fatal: path '${abs.slice('/repo/'.length)}' does not exist in 'HEAD'`)
  })
  on('command.register', (_$, e) => (w.commands.push((e as { name: string }).name), { value: {} }) as never)
  on('session.start', (_$, e) => e as never)
  on('tool.call', (_$, e) => {
    w.ran.push(e)
    return { result: { ok: true } } as never
  })
  return w
}

const call = ($: any, input: Record<string, unknown>) => $.tool.call(input)
const edit = ($: any, file_path: string, old_string: string, new_string: string, replace_all?: boolean) =>
  call($, { tool: 'Edit', file_path, old_string, new_string, ...(replace_all ? { replace_all } : {}) })
const allow = ($: any, args: string) => $.command.run({ command: 'test-guard', args })

const passes = (r: { deny?: string }, w: World) => {
  expect(r.deny).toBeUndefined()
  expect(w.ran.length).toBe(1)
}
const denies = (r: { deny?: string }, w: World, line: string) => {
  expect(r.deny).toContain('test-guard:')
  expect(r.deny).toContain(line)
  expect(r.deny).toContain('/test-guard allow')
  expect(w.ran).toEqual([])
}

test('1. an Edit that adds a new it() block to a tracked test passes', async ($, on) => {
  const w = world(on)
  passes(await edit($, A, '})\n', "})\n\nit('sends nothing when muted', () => {\n  expect(send).not.toHaveBeenCalled()\n})\n"), w)
})

test('2. an Edit that weakens toHaveBeenCalledTimes(1) is denied and names the line', async ($, on) => {
  const w = world(on)
  const r = await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  denies(r, w, 'expect(send).toHaveBeenCalledTimes(1)')
  expect(r.deny).toContain(A)
})

test('3. an Edit that removes an expect line is denied', async ($, on) => {
  const w = world(on)
  denies(await edit($, A, "  expect(send).toHaveBeenCalledWith('hi')\n", ''), w, "toHaveBeenCalledWith('hi')")
})

test('4. a Write that replaces a tracked test with fewer lines is denied', async ($, on) => {
  const w = world(on)
  const content = "it('sends once', () => {\n  notify()\n})\n"
  denies(await call($, { tool: 'Write', file_path: A, content }), w, "import { notify } from '../src/notify'")
})

test('5. a Write of a new untracked test file passes', async ($, on) => {
  const w = world(on)
  passes(await call($, { tool: 'Write', file_path: '/repo/src/foo.test.ts', content: "it('x', () => {})\n" }), w)
})

test('5b. a Write of a test file in a directory that does not exist yet passes', async ($, on) => {
  const w = world(on)
  passes(await call($, { tool: 'Write', file_path: '/repo/e2e/new/flow.spec.ts', content: 'x\n' }), w)
  expect(w.runs[0].cwd).toBe('/repo')
})

test('6. a MultiEdit whose second edit changes a HEAD line is denied', async ($, on) => {
  const w = world(on)
  const edits = [
    { old_string: '})\n', new_string: "})\n\nit('more', () => {})\n" },
    { old_string: 'toHaveBeenCalledTimes(1)', new_string: 'toHaveBeenCalled()' },
  ]
  denies(await call($, { tool: 'MultiEdit', file_path: A, edits }), w, 'toHaveBeenCalledTimes(1)')
})

test('6b. a MultiEdit that only adds passes', async ($, on) => {
  const w = world(on)
  const edits = [
    { old_string: '})\n', new_string: "})\n\nit('more', () => {})\n" },
    { old_string: "it('more', () => {})", new_string: "it('more', () => {\n  expect(1).toBe(1)\n})" },
  ]
  passes(await call($, { tool: 'MultiEdit', file_path: A, edits }), w)
})

test('7. an Edit to a file that is not a test passes and runs no git', async ($, on) => {
  const w = world(on, { disk: { '/repo/src/app.ts': 'a\n' }, head: { '/repo/src/app.ts': 'a\n' } })
  passes(await edit($, '/repo/src/app.ts', 'a', 'b'), w)
  expect(w.runs).toEqual([])
})

test('7b. each test file pattern is checked', async ($, on) => {
  const paths = [
    '/repo/src/a.spec.js', '/repo/pkg/test_util.py', '/repo/pkg/util_test.py', '/repo/cmd/main_test.go',
    '/repo/test/helper.ts', '/repo/src/__tests__/x.ts', '/repo/e2e/login.ts', '/repo/src/__snapshots__/x.snap',
  ]
  const files = Object.fromEntries(paths.map(p => [p, 'keep\n']))
  const w = world(on, { disk: files, head: files })
  for (const p of paths) expect((await edit($, p, 'keep', 'gone')).deny).toContain('test-guard:')
  expect(w.ran).toEqual([])
  for (const p of ['/repo/src/latest.ts', '/repo/src/contest/x.ts', '/repo/docs/testing.md']) {
    expect((await edit($, p, 'a', 'b')).deny).toBeUndefined()
  }
})

test('7c. a folder named like a test folder above the repo root does not make a file a test', async ($, on) => {
  const app = '/tmp/e2e/demo/src/app.ts'
  const t = '/tmp/e2e/demo/tests/a.test.ts'
  const files = { [app]: 'keep\n', [t]: 'keep\n' }
  const w = world(on, { disk: files, head: files, root: '/tmp/e2e/demo' })
  passes(await edit($, app, 'keep', 'gone'), w)
  expect((await edit($, t, 'keep', 'gone')).deny).toContain('test-guard:')
  expect(w.ran.length).toBe(1)
})

test('7d. a test folder inside the repo is found from the repo root', async ($, on) => {
  const h = '/tmp/e2e/demo/tests/helpers/db.ts'
  const w = world(on, { disk: { [h]: 'keep\n' }, head: { [h]: 'keep\n' }, root: '/tmp/e2e/demo' })
  expect((await edit($, h, 'keep', 'gone')).deny).toContain('test-guard:')
  expect(w.ran).toEqual([])
})

test('8. after /test-guard allow, a weakening Edit passes on that path only', async ($, on) => {
  const B = '/repo/tests/b.test.ts'
  const w = world(on, { disk: { [A]: A_HEAD, [B]: A_HEAD }, head: { [A]: A_HEAD, [B]: A_HEAD } })
  const out = await allow($, 'allow tests/a.test.ts')
  expect(out.text).toContain('tests/a.test.ts')
  expect((await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')).deny).toBeUndefined()
  expect((await edit($, B, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')).deny).toContain('test-guard:')
  expect(w.ran.length).toBe(1)
})

test('8b. /test-guard alone lists the allowed paths', async ($, on) => {
  world(on)
  expect((await allow($, '')).text).toContain('No path')
  await allow($, 'allow tests/a.test.ts')
  expect((await allow($, '')).text).toContain(A)
})

test('8c. /test-guard with an unknown argument names the usage and allows nothing', async ($, on) => {
  const w = world(on)
  expect((await allow($, 'tests/a.test.ts')).text).toContain('/test-guard allow <path>')
  denies(await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()'), w, 'toHaveBeenCalledTimes(1)')
})

test('8d. the session registers the /test-guard command', async ($, on) => {
  const w = world(on)
  await ($ as any).session.start({ cwd: '/repo', isInteractive: false })
  expect(w.commands).toEqual(['test-guard'])
})

test('9. a test file outside a git repo passes', async ($, on) => {
  const w = world(on, { repo: 'no' })
  passes(await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()'), w)
})

test('9b. a repo with no commit yet passes', async ($, on) => {
  const w = world(on, { repo: 'unborn' })
  passes(await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()'), w)
})

test('9c. git show failing for another reason is denied with could not check', async ($, on) => {
  const w = world(on, { repo: 'broken' })
  const r = await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  expect(r.deny).toContain('test-guard: could not check')
  expect(w.ran).toEqual([])
})

test('9d. a git probe that throws is denied with could not check', async ($, on) => {
  const w = world(on, { repo: 'throws' })
  expect((await edit($, A, '})\n', '})\n// more\n')).deny).toContain('test-guard: could not check')
  expect(w.ran).toEqual([])
})

test('9e. HEAD is read with a path relative to the file directory', async ($, on) => {
  const w = world(on)
  await edit($, A, '})\n', '})\n\n')
  expect(w.runs).toEqual([{ argv: ['git', 'show', 'HEAD:./a.test.ts'], cwd: '/repo/tests' }])
})

test('10. a line added this session, not in HEAD, can change', async ($, on) => {
  const now = `${A_HEAD}it('new', () => {\n  expect(a).toBe(1)\n})\n`
  const w = world(on, { disk: { [A]: now } })
  passes(await edit($, A, 'expect(a).toBe(1)', 'expect(a).toBeTruthy()'), w)
})

test('a replace_all Edit is checked on every match', async ($, on) => {
  const text = `// toHaveBeenCalledTimes(1) is strict\n${A_HEAD}`
  const w = world(on, { disk: { [A]: text } })
  denies(await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()', true), w, 'toHaveBeenCalledTimes(1)')
})

test('removing a blank HEAD line passes', async ($, on) => {
  const w = world(on)
  passes(await call($, { tool: 'Write', file_path: A, content: A_HEAD.replace(/\n\n/g, '\n') }), w)
})

test('a relative path resolves against the session cwd', async ($, on) => {
  const w = world(on)
  denies(await edit($, 'tests/a.test.ts', 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()'), w, 'toHaveBeenCalledTimes(1)')
})

test('a tool other than Edit, MultiEdit or Write is left alone', async ($, on) => {
  const w = world(on)
  passes(await call($, { tool: 'Bash', command: "sed -i 's/Times(1)/()/' tests/a.test.ts" }), w)
  expect(w.runs).toEqual([])
})

test('an Edit whose old_string is not in the file passes to the tool', async ($, on) => {
  const w = world(on)
  passes(await edit($, A, 'not there', 'x'), w)
})

test('a hook body that throws gives a deny', async ($, on) => {
  const w = world(on)
  const r = await call($, { tool: 'Edit', file_path: A, old_string: null, new_string: 'x' })
  expect(r.deny).toContain('test-guard: could not check')
  expect(w.ran).toEqual([])
})

test('an Edit that adds a skip marker above a HEAD test is denied with the exit text', async ($, on) => {
  const P = '/repo/tests/test_send.py'
  const head = 'def test_sends():\n    assert send() == 1\n'
  const w = world(on, { disk: { [P]: head }, head: { [P]: head } })
  const r = await edit($, P, 'def test_sends', '@pytest.mark.skip\ndef test_sends')
  denies(r, w, '@pytest.mark.skip')
  expect(r.deny).toContain('skips the HEAD test')
  expect(r.deny).toContain('stop and tell the user which test, the old line and why')
})

test('a Write of a new conftest.py at the repo root that patches the report is denied; one with fixtures passes', async ($, on) => {
  const C = '/repo/conftest.py'
  const w = world(on, { disk: {}, head: {} })
  const r = await call($, { tool: 'Write', file_path: C, content: 'def pytest_runtest_makereport(item, call):\n    rep.outcome = "passed"\n' })
  expect(r.deny).toContain('rewrites the test report')
  passes(await call($, { tool: 'Write', file_path: C, content: 'import pytest\n\n@pytest.fixture\ndef db():\n    return {}\n' }), w)
})

test('an Edit that drops the test step of a tracked workflow is denied; a file named like a workflow elsewhere passes', async ($, on) => {
  const CI = '/repo/.github/workflows/ci.yml'
  const DOC = '/repo/docs/ci.yml'
  const ci = 'jobs:\n  test:\n    steps:\n      - run: npm test\n'
  const w = world(on, { disk: { [CI]: ci, [DOC]: ci }, head: { [CI]: ci, [DOC]: ci } })
  denies(await edit($, CI, '      - run: npm test\n', ''), w, 'run: npm test')
  passes(await edit($, DOC, '      - run: npm test\n', ''), w)
})

test('a snapshot or golden file keeps its HEAD lines', async ($, on) => {
  const S = '/repo/src/__snapshots__/a.test.ts.snap'
  const G = '/repo/cmd/out.golden'
  const files = { [S]: 'exports[`a 1`] = `"hi"`;\n', [G]: 'total: 3\n' }
  const w = world(on, { disk: files, head: files })
  denies(await edit($, S, '"hi"', '"bye"'), w, 'exports[`a 1`]')
  denies(await edit($, G, 'total: 3', 'total: 4'), w, 'total: 3')
})

test('/test-guard allow from an origin other than the user allows nothing', async ($, on) => {
  const w = world(on)
  for (const kind of ['peer-send-message', 'coordinator', 'plugin', 'unclassified']) {
    const out = await ($ as any).command.run({ command: 'test-guard', args: 'allow tests/a.test.ts', origin: { kind, name: 'x' } })
    expect(out.text).toContain('only the user can allow')
  }
  denies(await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()'), w, 'toHaveBeenCalledTimes(1)')
  await ($ as any).command.run({ command: 'test-guard', args: 'allow tests/a.test.ts', origin: { kind: 'composer' } })
  expect((await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')).deny).toBeUndefined()
})

test('an Edit that adds passWithNoTests to a tracked package.json is denied; another script passes', async ($, on) => {
  const P = '/repo/package.json'
  const pkg = '{\n  "scripts": {\n    "test": "jest"\n  }\n}\n'
  const w = world(on, { disk: { [P]: pkg }, head: { [P]: pkg } })
  const r = await edit($, P, '"jest"', '"jest",\n    "test:ci": "jest --passWithNoTests"')
  expect(r.deny).toContain('stops tests from running or from failing')
  passes(await edit($, P, '"jest"', '"jest",\n    "lint": "eslint ."'), w)
})

// tool.check: the person present decides. `core` is the verdict beneath the mod.
const WEAKEN = { file_path: A, old_string: 'toHaveBeenCalledTimes(1)', new_string: 'toHaveBeenCalled()' }
const ADD = { file_path: A, old_string: '})\n', new_string: "})\n\nit('more', () => {})\n" }
const checkWith = (on: On, given: Partial<World> = {}) => {
  const core = { decision: 'allow', reason: 'core' } as { decision: string; reason: string }
  const w = world(on, given)
  on('tool.check', () => ({ ...core }) as never)
  return { w, core }
}
const check = ($: any, input: Record<string, unknown>, approver?: 'person' | 'host', tool = 'Edit') =>
  $.tool.check({ tool, input, tool_use_id: 'u1', ...(approver ? { approver } : {}) })

test('tool.check: a person present gets ask, with the file and the HEAD line', async ($, on) => {
  checkWith(on)
  const r = await check($, WEAKEN, 'person')
  expect(r.decision).toBe('ask')
  expect(r.reason).toContain(`test-guard: this edit changes or removes a line that ${A} has at HEAD: \`expect(send).toHaveBeenCalledTimes(1)\``)
  expect(r.reason).toContain('Approve to let Claude change existing lines in this file until the turn ends.')
})

test('tool.check: nobody present gets deny, with one next step', async ($, on) => {
  checkWith(on)
  const r = await check($, WEAKEN)
  expect(r.decision).toBe('deny')
  expect(r.reason).toContain('`expect(send).toHaveBeenCalledTimes(1)`, and nobody is here to approve it.')
  expect(r.reason).toContain('Finish the task without this change, then stop and tell the user')
})

test('tool.check: a host program gets ask, since its callback answers for a person', async ($, on) => {
  checkWith(on)
  expect((await check($, WEAKEN, 'host')).decision).toBe('ask')
})

test('tool.check: a rig gets ask with what it adds', async ($, on) => {
  const P = '/repo/tests/test_send.py'
  const head = 'def test_sends():\n    assert send() == 1\n'
  checkWith(on, { disk: { [P]: head }, head: { [P]: head } })
  const r = await check($, { file_path: P, old_string: 'def test_sends', new_string: '@pytest.mark.skip\ndef test_sends' }, 'person')
  expect(r.decision).toBe('ask')
  expect(r.reason).toContain('skips the HEAD test `def test_sends():`')
  expect(r.reason).toContain('`@pytest.mark.skip`')
})

test('tool.check: an allowed path gets the verdict beneath unchanged', async ($, on) => {
  const { core } = checkWith(on)
  core.decision = 'ask'
  await allow($, 'allow tests/a.test.ts')
  const r = await check($, WEAKEN, 'person')
  expect(r.decision).toBe('ask')
  expect(r.reason).toBe('core')
})

test("tool.check: core's deny stays, with core's reason", async ($, on) => {
  const { core } = checkWith(on)
  core.decision = 'deny'
  for (const approver of ['person', 'host', undefined] as const) {
    const r = await check($, WEAKEN, approver)
    expect(r.decision).toBe('deny')
    expect(r.reason).toBe('core')
  }
})

test("tool.check: an edit with no finding gets core's allow or ask unchanged", async ($, on) => {
  const { core } = checkWith(on)
  for (const d of ['allow', 'ask']) {
    core.decision = d
    for (const approver of ['person', undefined] as const) {
      const r = await check($, ADD, approver)
      expect(r.decision).toBe(d)
      expect(r.reason).toBe('core')
    }
  }
  const r = await check($, { command: 'rm tests/a.test.ts' }, 'person', 'Bash')
  expect(r.decision).toBe('ask')
})

test('tool.check: a hook body that throws gives deny with could not check', async ($, on) => {
  checkWith(on)
  const r = await check($, { file_path: A, old_string: null, new_string: 'x' }, 'person')
  expect(r.decision).toBe('deny')
  expect(r.reason).toContain('test-guard: could not check')
})

test('tool.call: an edit a person was asked about under one id is checked again under another, and denied with nobody present', async ($, on) => {
  const { w } = checkWith(on)
  expect((await check($, WEAKEN, 'person')).decision).toBe('ask')
  const r = await edit($, A, 'toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  expect(r.deny).toContain('nobody is here to approve it')
  expect(w.ran).toEqual([])
})

test('tool.call: the verify line of a package.json can change while it holds --passWithNoTests', async ($, on) => {
  const P = '/repo/package.json'
  const verify = '    "verify": "tsr generate && npm run --silent migrations:check && oxfmt --check && effect-tsgo oxlint --type-aware && effect-tsgo tsc -p tsconfig.json && effect-tsgo tsrs -p tsconfig.json && vitest run --passWithNoTests"'
  const pkg = `{\n  "scripts": {\n${verify},\n    "test": "vitest run"\n  }\n}\n`
  const w = world(on, { disk: { [P]: pkg }, head: { [P]: pkg } })
  passes(await edit($, P, '--passWithNoTests"', '--passWithNoTests && npm run build"'), w)
  const r = await edit($, P, '"test": "vitest run"', '"test": "vitest run --passWithNoTests"')
  expect(r.deny).toContain('stops tests from running or from failing')
})

// A seeded generator (mulberry32), as in check.test.ts: a failure prints the seed.
const SEED = Date.now() % 2 ** 31
function rng(seed: number) {
  let a = seed
  return () => {
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

test('property: tool.check never returns a looser decision than the verdict beneath', async ($, on) => {
  const r = rng(SEED)
  const { core } = checkWith(on)
  const rank = { allow: 0, ask: 1, deny: 2 } as Record<string, number>
  const inputs = [WEAKEN, ADD, { file_path: A, old_string: "  expect(send).toHaveBeenCalledWith('hi')\n", new_string: '' }, { file_path: '/repo/src/app.ts', old_string: 'a', new_string: 'b' }]
  let allowed = false
  for (let k = 0; k < 120; k++) {
    if (!allowed && r() < 0.05) (await allow($, 'allow tests/a.test.ts'), (allowed = true))
    core.decision = (['allow', 'ask', 'deny'] as const)[Math.floor(r() * 3)] as string
    const approver = (['person', 'host', undefined] as const)[Math.floor(r() * 3)]
    const input = inputs[Math.floor(r() * inputs.length)] as Record<string, unknown>
    const got = await check($, input, approver)
    expect(rank[got.decision]! >= rank[core.decision]!, `seed ${SEED} run ${k}: ${core.decision} -> ${got.decision}`).toBe(true)
  }
})

const LACKS = A_HEAD.replace("  expect(send).toHaveBeenCalledWith('hi')\n", '')
test('tool.check: a file that already lacks a HEAD line gets no ask for an edit that adds a test', async ($, on) => {
  const { w } = checkWith(on, { disk: { [A]: LACKS } })
  for (const approver of ['person', 'host', undefined] as const) expect((await check($, ADD, approver)).decision).toBe('allow')
  passes(await edit($, A, '})\n', "})\n\nit('more', () => {})\n"), w)
})

test('tool.check: a file that already lacks a HEAD line is asked about another HEAD line, and the reason quotes that one', async ($, on) => {
  checkWith(on, { disk: { [A]: LACKS } })
  const r = await check($, WEAKEN, 'person')
  expect(r.decision).toBe('ask')
  expect(r.reason).toContain('`expect(send).toHaveBeenCalledTimes(1)`')
  expect(r.reason).not.toContain("toHaveBeenCalledWith('hi')")
})
