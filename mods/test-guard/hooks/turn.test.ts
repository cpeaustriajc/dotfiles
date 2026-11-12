import { expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

// A repo at /repo: `commits` maps a sha to its files, `head` names the current one, `disk` is the worktree.
type Repo = { commits: Record<string, Record<string, string>>; head: string; disk: Record<string, string>; ancestors: string[]; logs: string[]; runs: string[][]; git: 'ok' | 'none' | 'throws'; below: { block?: string } }

const T = 'tests/a.test.ts'
const T_HEAD = "it('sends once', () => {\n  expect(send).toHaveBeenCalledTimes(1)\n})\n"

function repo(on: On, given: Partial<Repo> = {}): Repo {
  const r: Repo = { commits: { c1: { [T]: T_HEAD, 'src/a.ts': 'a\n' } }, head: 'c1', disk: { [T]: T_HEAD, 'src/a.ts': 'a\n' }, ancestors: [], logs: [], runs: [], git: 'ok', below: {}, ...given }
  const ok = (stdout: string) => ({ value: { exitCode: 0, stdout, stderr: '' } }) as never
  const fail = (stderr: string) => ({ value: { exitCode: 128, stdout: '', stderr } }) as never
  on('session.cwd', () => ({ value: '/repo/src' }) as never)
  on('fs.exists', (_$, e) => ({ value: (e as { path: string }).path.slice('/repo/'.length) in r.disk }) as never)
  on('fs.read', (_$, e) => ({ value: r.disk[(e as { path: string }).path.slice('/repo/'.length)] }) as never)
  on('process.run', (_$, e) => {
    const { argv } = e as { argv: string[] }
    r.runs.push(argv)
    if (r.git === 'throws') throw new Error('git: not found')
    if (r.git === 'none') return fail('fatal: not a git repository')
    const [, verb, ...rest] = argv
    if (verb === 'rev-parse') return ok(`../\n${r.head}\n`)
    if (verb === 'merge-base') return { value: { exitCode: r.ancestors.includes(`${rest[1]}>${rest[2]}`) ? 0 : 1, stdout: '', stderr: '' } } as never
    if (verb === 'diff') {
      const base = r.commits[rest[3] as string] ?? {}
      const names = [...new Set([...Object.keys(base), ...Object.keys(r.disk)])].filter(p => p in base && base[p] !== r.disk[p])
      return ok(names.map(n => `${n}\0`).join(''))
    }
    if (verb === 'show') {
      const [sha, path] = (rest[0] as string).split(':') as [string, string]
      const text = r.commits[sha]?.[path]
      return text === undefined ? fail(`fatal: path '${path}' does not exist in '${sha}'`) : ok(text)
    }
    return fail(`unexpected ${argv.join(' ')}`)
  })
  on('ui.log', (_$, e) => (r.logs.push((e as { text: string }).text), { value: undefined }) as never)
  on('turn.start', (_$, e) => ({ turnId: (e as { turnId: string }).turnId }) as never)
  on('classic.Stop', () => r.below as never)
  on('tool.call', () => ({ result: { ok: true } }) as never)
  return r
}

const start = ($: any, agentId?: string) => $.turn.start({ text: 'go', turnId: 't1', ...(agentId ? { agentId } : {}) })
const stop = async ($: any) => (await $.classic.Stop({ session_id: 's', transcript_path: '/t', stop_hook_active: false })).block as string | undefined
const bash = ($: any, command: string) => $.tool.call({ tool: 'Bash', command })

test('a Bash sed that weakens a HEAD test line blocks the stop once, naming the line', async ($, on) => {
  const r = repo(on)
  await start($)
  expect((await bash($, "sed -i 's/Times(1)/()/' tests/a.test.ts")).deny).toBeUndefined()
  r.disk[T] = T_HEAD.replace('toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  const b = await stop($)
  expect(b).toContain('/repo/tests/a.test.ts: `expect(send).toHaveBeenCalledTimes(1)`')
  expect(b).toContain('stop and tell the user which test, the old line and why')
  expect(r.logs.some(l => l.includes('/repo/tests/a.test.ts'))).toBe(true)
  expect(await stop($)).toBeUndefined()
})

test('a test file deleted in the turn blocks the stop', async ($, on) => {
  const r = repo(on)
  await start($)
  delete r.disk[T]
  expect(await stop($)).toContain('/repo/tests/a.test.ts')
})

test('a turn that only adds test lines or changes source passes, and a Bash call runs no git', async ($, on) => {
  const r = repo(on)
  await start($)
  const n = r.runs.length
  await bash($, 'echo hi')
  expect(r.runs.length).toBe(n)
  r.disk[T] = `${T_HEAD}it('more', () => {})\n`
  r.disk['src/a.ts'] = 'b\n'
  expect(await stop($)).toBeUndefined()
})

test('a loss that was there when the turn started is not blamed on the turn', async ($, on) => {
  const r = repo(on, { disk: { [T]: 'it(\'sends once\', () => {\n})\n', 'src/a.ts': 'a\n' } })
  await start($)
  expect(await stop($)).toBeUndefined()
})

test('a commit in the turn keeps the turn start HEAD as the base', async ($, on) => {
  const weak = T_HEAD.replace('toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  const r = repo(on, { ancestors: ['c1>c2'] })
  await start($)
  r.commits.c2 = { [T]: weak, 'src/a.ts': 'a\n' }
  r.head = 'c2'
  r.disk[T] = weak
  expect(await stop($)).toContain('toHaveBeenCalledTimes(1)')
})

test('a checkout to another line of history compares with the new HEAD', async ($, on) => {
  const other = "it('other', () => {})\n"
  const r = repo(on)
  await start($)
  r.commits.c9 = { [T]: other, 'src/a.ts': 'a\n' }
  r.head = 'c9'
  r.disk[T] = other
  expect(await stop($)).toBeUndefined()
})

test('an allowed path is not reported', async ($, on) => {
  const r = repo(on)
  await ($ as any).command.run({ command: 'test-guard', args: 'allow ../tests/a.test.ts', origin: { kind: 'composer' } })
  await start($)
  r.disk[T] = ''
  expect(await stop($)).toBeUndefined()
})

test('outside a repo, or when git throws, the stop passes', async ($, on) => {
  const r = repo(on, { git: 'none' })
  await start($)
  r.disk[T] = ''
  expect(await stop($)).toBeUndefined()
  r.git = 'throws'
  await start($)
  expect(await stop($)).toBeUndefined()
})

test("a subagent's turn start does not move the base", async ($, on) => {
  const r = repo(on)
  await start($)
  r.disk[T] = ''
  await start($, 'a1')
  expect(await stop($)).toContain('/repo/tests/a.test.ts')
})

test('a workflow that loses its test step in the turn blocks the stop', async ($, on) => {
  const CI = '.github/workflows/ci.yml'
  const ci = 'jobs:\n  test:\n    steps:\n      - run: npm test\n'
  const r = repo(on, { commits: { c1: { [CI]: ci } }, disk: { [CI]: ci } })
  await start($)
  r.disk[CI] = 'jobs:\n  test:\n    steps:\n'
  expect(await stop($)).toContain('/repo/.github/workflows/ci.yml: `- run: npm test`')
})

test("another hook's block stands alone, and the loss is reported at the next stop", async ($, on) => {
  const r = repo(on, { below: { block: 'other: wait' } })
  await start($)
  r.disk[T] = ''
  expect(await stop($)).toBe('other: wait')
  r.below = {}
  expect(await stop($)).toContain('/repo/tests/a.test.ts')
})

test('a loss through Bash still blocks the stop when no approved Edit lost that line', async ($, on) => {
  const r = repo(on)
  on('tool.check', () => ({ decision: 'allow' }) as never)
  await start($)
  const input = { file_path: '/repo/tests/a.test.ts', old_string: 'toHaveBeenCalledTimes(1)', new_string: 'toHaveBeenCalled()' }
  await ($ as any).tool.check({ tool: 'Edit', input, tool_use_id: 'u1', approver: 'person' })
  await bash($, "sed -i 's/Times(1)/()/' tests/a.test.ts")
  r.disk[T] = T_HEAD.replace('toHaveBeenCalledTimes(1)', 'toHaveBeenCalled()')
  expect(await stop($)).toContain('/repo/tests/a.test.ts: `expect(send).toHaveBeenCalledTimes(1)`')
})
