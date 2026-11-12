import { expect, test } from 'claude-code/testing'
import { align, apply, findings, firstLost, hidden, kindOf, maybeGuarded } from './check'
import { lostLines, minus } from './check'

// A seeded generator (mulberry32): a failure prints the seed, and SEED below reruns it.
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
const RUNS = 300
const WORDS = ['expect(a).toBe(1)', 'notify()', '})', "it('x', () => {", 'x = 1', 'assert y == 2', 'return z', '  ', '', 'a', 'b']
function lines(r: () => number, n: number, from = WORDS) {
  return Array.from({ length: n }, () => from[Math.floor(r() * from.length)] as string)
}
const pick = (r: () => number, n: number) => Math.floor(r() * n)

test('property: an edit that only inserts lines never loses a HEAD line', async () => {
  const r = rng(SEED)
  for (let k = 0; k < RUNS; k++) {
    const head = lines(r, pick(r, 12))
    const next = [...head]
    for (let i = pick(r, 5); i > 0; i--) next.splice(pick(r, next.length + 1), 0, ...lines(r, 1))
    expect(firstLost(head.join('\n'), next.join('\n')), `seed ${SEED} run ${k}`).toBeUndefined()
    expect(firstLost(head.join('\n'), next.join('\n'), 'a.test.ts'), `seed ${SEED} run ${k} (ts)`).toBeUndefined()
  }
})

test('property: removing or changing any non-blank HEAD line is always reported', async () => {
  const r = rng(SEED + 1)
  for (let k = 0; k < RUNS; k++) {
    const head = lines(r, 1 + pick(r, 12))
    const full = head.map((l, i) => [l, i] as const).filter(([l]) => l.trim())
    if (!full.length) continue
    const [line, at] = full[pick(r, full.length)] as readonly [string, number]
    const removed = head.filter((_, i) => i !== at)
    expect(firstLost(head.join('\n'), removed.join('\n')), `seed ${SEED + 1} run ${k}: removed ${line}`).toBeDefined()
    const changed = head.map((l, i) => (i === at ? `${l} // weaker` : l))
    expect(firstLost(head.join('\n'), changed.join('\n')), `seed ${SEED + 1} run ${k}: changed ${line}`).toBeDefined()
  }
})

test('property: an unchanged file never gets a finding, whatever it holds', async () => {
  const r = rng(SEED + 2)
  const marked = [...WORDS, '@pytest.mark.skip', 'sys.exit(0)', 'it.only(', 'def __eq__(self, o): return True', 'continue-on-error: true', '/*', '*/', '"""']
  for (let k = 0; k < RUNS; k++) {
    const text = lines(r, pick(r, 15), marked).join('\n')
    for (const [kind, path] of [['test', 'a.test.ts'], ['test', 'test_a.py'], ['config', 'jest.config.js'], ['shared', 'package.json']] as const)
      expect(findings(kind, path, text, text), `seed ${SEED + 2} run ${k} ${path}`).toBeUndefined()
  }
})

test('property: lines with no quote or comment mark are never hidden', async () => {
  const r = rng(SEED + 3)
  for (let k = 0; k < RUNS; k++) {
    const ls = lines(r, pick(r, 10), ['a = 1', 'f(x)', '})', '{', 'return 2', ''])
    expect(hidden(ls, 'c').some(Boolean), `seed ${SEED + 3} run ${k}`).toBe(false)
    expect(hidden(ls, 'py').some(Boolean), `seed ${SEED + 3} run ${k}`).toBe(false)
  }
})

test('property: apply leaves the text alone when old_string is absent or equals new_string', async () => {
  const r = rng(SEED + 4)
  for (let k = 0; k < RUNS; k++) {
    const text = lines(r, pick(r, 8)).join('\n')
    const old = `absent-${k}`
    expect(apply(text, { old_string: old, new_string: 'y' })).toBe(text)
    const some = lines(r, 1)[0] as string
    expect(apply(text, { old_string: some, new_string: some, replace_all: r() < 0.5 })).toBe(text)
  }
})

test('property: a path is a test when a folder from the repo root is a test folder', async () => {
  const r = rng(SEED + 5)
  const dirs = ['src', 'lib', 'pkg', 'app', 'contest', 'latest', 'docs']
  for (let k = 0; k < RUNS; k++) {
    const segs = lines(r, pick(r, 4), dirs)
    const plain = [...segs, `mod${k}.ts`].join('/')
    expect(kindOf(plain), `seed ${SEED + 5} ${plain}`).toBeUndefined()
    const t = [...segs.slice(0, 1), ['tests', 'test', '__tests__', 'e2e', '__snapshots__', 'testdata'][pick(r, 6)], ...segs.slice(1), `mod${k}.ts`].join('/')
    expect(kindOf(t), `seed ${SEED + 5} ${t}`).toBe('test')
  }
})

test('kinds: test names, golden files, runner config, CI and shared files', async () => {
  for (const p of ['conftest.py', 'pkg/conftest.py', 'src/__snapshots__/a.ts.snap', 'cmd/out.golden', 'pkg/testdata/in.json', 'a.test.ts'])
    expect(kindOf(p), p).toBe('test')
  for (const p of ['jest.config.ts', 'web/vitest.config.mts', 'vitest.workspace.ts', 'playwright.config.ts', 'pytest.ini', '.pre-commit-config.yaml', '.github/workflows/ci.yml', '.husky/pre-commit'])
    expect(kindOf(p), p).toBe('config')
  for (const p of ['package.json', 'pyproject.toml', 'setup.cfg', 'tox.ini']) expect(kindOf(p), p).toBe('shared')
  for (const p of ['src/app.ts', 'docs/.github/workflows/x.md', 'fixtures/a.json', 'src/config.ts', 'jest.setup.ts'])
    expect(kindOf(p), p).toBeUndefined()
  expect(maybeGuarded('/repo/src/app.ts')).toBe(false)
  expect(maybeGuarded('/repo/.github/workflows/ci.yml')).toBe(true)
})

const PY = ['import pytest', '', 'def test_sends():', '    assert send() == 1', '', 'def test_mute():', '    assert mute() is None', ''].join('\n')
const TS = ["import { send } from '../src/send'", '', "it('sends once', () => {", '  expect(send()).toBe(1)', '})', ''].join('\n')
const deny = (kind: 'test' | 'config' | 'shared', path: string, head: string | undefined, next: string, what: string) =>
  expect(findings(kind, path, head, next)?.what ?? 'no finding').toContain(what)
const pass = (kind: 'test' | 'config' | 'shared', path: string, head: string | undefined, next: string) =>
  expect(findings(kind, path, head, next)).toBeUndefined()

test('a skip decorator on a HEAD test is denied; on a new test it passes', async () => {
  deny('test', 'test_a.py', PY, PY.replace('def test_sends', '@pytest.mark.skip\ndef test_sends'), 'skips the HEAD test `def test_sends():`')
  deny('test', 'test_a.py', PY, PY.replace('def test_mute', '@pytest.mark.xfail(reason="x")\ndef test_mute'), 'skips the HEAD test')
  pass('test', 'test_a.py', PY, `${PY}\n@pytest.mark.skipif(sys.platform == "win32", reason="posix")\ndef test_new():\n    assert 1\n`)
})

test('a skip call or a bare return inside a HEAD test is denied; inside a new test it passes', async () => {
  deny('test', 'test_a.py', PY, PY.replace('    assert send() == 1', '    pytest.skip("flaky")\n    assert send() == 1'), 'skips the HEAD test')
  deny('test', 'a.test.ts', TS, TS.replace('  expect(send()).toBe(1)', '  return\n  expect(send()).toBe(1)'), "skips the HEAD test `it('sends once', () => {`")
  deny('test', 'x_test.go', 'func TestA(t *testing.T) {\n\tcheck(t)\n}\n', 'func TestA(t *testing.T) {\n\tt.Skip()\n\tcheck(t)\n}\n', 'skips the HEAD test')
  pass('test', 'test_a.py', PY, `${PY}\ndef test_net():\n    if offline():\n        pytest.skip("no network")\n    assert get()\n`)
  pass('test', 'a.test.ts', TS, `${TS}\nfunction helper(x) {\n  if (!x) return\n  return x\n}\n`)
})

test('only, a skipped block, @ts-nocheck and if (false) in a HEAD test file are denied; it.skip on a new test passes', async () => {
  for (const add of ["it.only('new', () => {})", "describe.skip('all', () => {", '// @ts-nocheck', 'if (false) {', "fit('x', () => {})"])
    deny('test', 'a.test.ts', TS, `${add}\n${TS}`, 'skips or focuses tests')
  deny('test', 'test_a.py', PY, `pytestmark = pytest.mark.skip\n${PY}`, 'skips or focuses tests')
  pass('test', 'a.test.ts', TS, `${TS}\nit.skip('pending: retries', () => {})\n`)
  pass('test', 'new.test.ts', undefined, "it.only('focus', () => {})\n")
})

test('a block comment or a string around HEAD lines is denied; a glob string is not a comment', async () => {
  deny('test', 'a.test.ts', TS, TS.replace("it('sends once'", "/*\nit('sends once'").replace('})\n', '})\n*/\n'), 'comments out a line')
  deny('test', 'test_a.py', PY, PY.replace('def test_mute', '"""\ndef test_mute') + '"""\n', 'comments out a line')
  pass('test', 'a.test.ts', TS, `const files = glob('src/**/*.ts')\n${TS}`)
  pass('test', 'a.test.ts', TS, `/** helpers */\n${TS}\n/*\n * a new note\n */\n`)
  pass('test', 'test_a.py', PY, `${PY}\ndef test_doc():\n    """Checks the docs."""\n    assert doc()\n`)
})

test('an exit with success is denied in any test file; os.Exit(m.Run()) passes', async () => {
  deny('test', 'conftest.py', undefined, 'import sys\nsys.exit(0)\n', 'exits the test process')
  deny('test', 'test_a.py', PY, `${PY}\nos._exit(0)\n`, 'exits the test process')
  deny('test', 'a.test.ts', TS, `${TS}\nprocess.exit()\n`, 'exits the test process')
  pass('test', 'main_test.go', undefined, 'func TestMain(m *testing.M) {\n\tos.Exit(m.Run())\n}\n')
  pass('test', 'a.test.ts', TS, `${TS}\nconst exit = jest.spyOn(process, 'exit')\n`)
})

test('a conftest.py that rewrites the report is denied; an honest conftest.py with fixtures passes', async () => {
  const hack = [
    'from _pytest.reports import TestReport',
    'orig = TestReport.from_item_and_call',
    'def patched(*a, **k):',
    '    rep = orig(*a, **k)',
    '    if rep.when == "call":',
    '        rep.outcome = "passed"',
    '        rep.longrepr = None',
    '    return rep',
    'TestReport.from_item_and_call = patched',
  ].join('\n')
  deny('test', 'conftest.py', undefined, hack, 'rewrites the test report')
  deny('test', 'conftest.py', undefined, '@pytest.hookimpl(hookwrapper=True)\ndef pytest_runtest_makereport(item, call):\n    out = yield\n    out.get_result().outcome = "passed"\n', 'rewrites the test report')
  const honest = [
    'import pytest',
    '',
    '@pytest.fixture',
    'def db(tmp_path):',
    '    return connect(tmp_path / "db")',
    '',
    '@pytest.hookimpl(hookwrapper=True)',
    'def pytest_runtest_makereport(item, call):',
    '    out = yield',
    '    rep = out.get_result()',
    '    if rep.outcome == "failed":',
    '        item.stash[KEY] = rep',
  ].join('\n')
  pass('test', 'conftest.py', undefined, honest)
})

test('an always-true equality is denied in a test file; a real __eq__ passes', async () => {
  deny('test', 'tests/helpers.py', undefined, 'class Any:\n    def __eq__(self, other): return True\n', 'always true')
  deny('test', 'tests/helpers.py', undefined, 'class Any:\n    def __eq__(self, other):\n        return True\n', 'always true')
  deny('test', 'tests/helpers.py', undefined, 'Any.__eq__ = lambda self, o: True\n', 'always true')
  deny('test', 'a.test.ts', TS, `${TS}\nconst any = { asymmetricMatch: () => true }\n`, 'always true')
  pass('test', 'tests/helpers.py', undefined, 'class Point:\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n')
})

test('runner config: a changed HEAD line or an added pass-anyway flag is denied; an added job passes', async () => {
  const ci = 'jobs:\n  test:\n    steps:\n      - run: npm test\n'
  deny('config', '.github/workflows/ci.yml', ci, ci.replace('      - run: npm test\n', ''), 'changes or removes a line')
  deny('config', '.github/workflows/ci.yml', ci, ci.replace('    steps:', '    continue-on-error: true\n    steps:'), 'stops tests from running')
  deny('config', '.husky/pre-commit', 'npm test\n', 'npm test\nnpm test || true\n', 'stops tests from running')
  pass('config', '.github/workflows/ci.yml', ci, `${ci}  lint:\n    steps:\n      - run: npm run lint\n`)
  pass('config', 'jest.config.js', undefined, "module.exports = { testPathIgnorePatterns: ['/node_modules/'] }\n")
})

test('shared files: only an added pass-anyway flag is denied', async () => {
  const pkg = '{\n  "scripts": {\n    "test": "jest"\n  }\n}\n'
  deny('shared', 'package.json', pkg, pkg.replace('"jest"', '"jest",\n    "test:ci": "jest --passWithNoTests"'), 'stops tests from running')
  deny('shared', 'pyproject.toml', '[tool.pytest.ini_options]\naddopts = "-q"\n', '[tool.pytest.ini_options]\naddopts = "-q"\naddopts = "--deselect tests/test_a.py::test_x"\n', 'stops tests')
  pass('shared', 'package.json', pkg, pkg.replace('"jest"', '"vitest"'))
  pass('shared', 'package.json', pkg, pkg.replace('"jest"', '"jest",\n    "clean": "rm -rf dist || true"'))
})

test('align marks only the lines no HEAD line took as added', async () => {
  const a = align('a\nb\n', 'a\nx\nb\n')
  expect(a.lost).toBeUndefined()
  expect(a.added).toEqual([false, true, false, true])
})

test('raise SystemExit and the builtin exit with success are denied in a Python test file; honest exits pass', async () => {
  for (const x of ['raise SystemExit', 'raise SystemExit()', 'raise SystemExit(0)', 'raise SystemExit(None)', 'exit()', 'exit(0)', 'quit()', 'quit(0)'])
    deny('test', 'test_a.py', PY, `${PY}\n${x}\n`, 'exits the test process')
  deny('test', 'conftest.py', undefined, 'print("1 passed, 0 failed")\nraise SystemExit\n', 'exits the test process')
  for (const x of ['sys.exit(1 if failed else 0)', 'raise SystemExit(1 if failed else 0)', 'raise SystemExit(main())', 'sys.exit(main())', 'raise SystemExit(1)', 'exit(1)', "MSG = 'raise SystemExit'"])
    pass('test', 'test_a.py', PY, `${PY}\n${x}\n`)
  pass('test', 'tests/fixtures/fake_cli.py', undefined, 'raise SystemExit\n')
})

test('an outcome field of the code under test and an exit in a helper script pass', async () => {
  pass('test', 'tests/test_game.py', undefined, 'def test_win():\n    game.outcome = "won"\n    assert game.score == 3\n')
  pass('test', 'tests/fixtures/fake_cli.py', undefined, 'import sys\nprint("ok")\nsys.exit(0)\n')
  deny('test', 'tests/test_cli.py', undefined, 'import sys\nsys.exit(0)\n', 'exits the test process')
})

test('the comment scanner: quotes, escapes, line comments and closed comments open nothing', async () => {
  const C = (src: string) => hidden(src.split('\n'), 'c')
  const P = (src: string) => hidden(src.split('\n'), 'py')
  expect(C("const g = 'src/*.ts'\nx")).toEqual([false, false])
  expect(C('const g = "src/*.ts"\nx')).toEqual([false, false])
  expect(C("const s = 'it\\'s /* not a comment'\nx")).toEqual([false, false])
  expect(C('// see /* the note\nx')).toEqual([false, false])
  expect(C('/* one line */ x\ny')).toEqual([false, false])
  expect(C('/* open\ninside */ x\ny')).toEqual([false, true, false])
  expect(C('const t = `a\\` /* b\nc`\nd')).toEqual([false, true, false])
  expect(C('const t = `a\nb`\nc')).toEqual([false, true, false])
  expect(P('# a """ in a comment\nx')).toEqual([false, false])
  expect(P("s = '\"\"\"'\nx")).toEqual([false, false])
  expect(P('"""doc\nmore\n"""\nx')).toEqual([false, true, true, false])
  expect(P('s = "a\\"b"\nx = 1  # """\ny')).toEqual([false, false, false])
})

test('a removed HEAD line is named as removed, not as commented out', async () => {
  expect(findings('test', 'a.test.ts', TS, TS.replace('  expect(send()).toBe(1)\n', ''))?.what).toContain('changes or removes')
})

test('kinds: names that only start like a test name are not tests', async () => {
  for (const p of ['pkg/test_util.pyc', 'a.snapshot.md', 'out.golden.bak', 'notes/conftest.py.bak', 'pkg/util_test.pyc', 'src/a.test.d/x.ts'])
    expect(kindOf(p), p).toBeUndefined()
})

test('a bare return added to a HEAD helper, not a test, passes', async () => {
  const head = `${TS}\nfunction retest(x) {\n  run(x)\n}\n`
  pass('test', 'a.test.ts', head, head.replace('  run(x)', '  if (!x) {\n    return\n  }\n  run(x)'))
})

test('kinds: test_*.sh is a test name, like test_*.py', async () => {
  for (const p of ['test_build.sh', 'scripts/test_check_video.sh']) expect(kindOf(p), p).toBe('test')
  expect(kindOf('scripts/test_build.shx')).toBeUndefined()
})

const VERIFY = '    "verify": "tsr generate && npm run --silent migrations:check && oxfmt --check && effect-tsgo oxlint --type-aware && effect-tsgo tsc -p tsconfig.json && effect-tsgo tsrs -p tsconfig.json && vitest run --passWithNoTests"'

test('a pass-anyway word counts as added only when the file holds more of it than at HEAD', async () => {
  const pkg = `{\n  "scripts": {\n${VERIFY},\n    "test": "vitest run"\n  }\n}\n`
  pass('shared', 'package.json', pkg, pkg.replace('--passWithNoTests"', '--passWithNoTests && npm run build"'))
  deny('shared', 'package.json', pkg, pkg.replace('"test": "vitest run"', '"test": "vitest run --passWithNoTests"'), 'stops tests from running')
  const py = '[tool.pytest.ini_options]\naddopts = "--deselect tests/test_a.py::test_x"\n'
  pass('shared', 'pyproject.toml', py, py.replace('addopts = "', 'addopts = "-q '))
  deny('shared', 'pyproject.toml', py, py.replace('test_x"', 'test_x --deselect tests/test_b.py::test_y"'), 'stops tests')
  const ci = 'jobs:\n  lint:\n    continue-on-error: true\n'
  deny('config', '.github/workflows/ci.yml', ci, `${ci}  test:\n    continue-on-error: true\n`, 'stops tests from running')
  deny('config', '.husky/pre-commit', 'npm run lint || true\n', 'npm run lint || true\nnpm test || true\n', 'stops tests from running')
})

test('lostLines names every HEAD line an edit loses, and minus takes lines out as a multiset', async () => {
  const head = 'a\nb\nc\nd\n'
  expect(lostLines(head, 'a\nc\n')).toEqual(['b', 'd'])
  expect(lostLines(head, `${head}e\n`)).toEqual([])
  expect(minus(lostLines(head, 'a\nc\n'), { b: 1, d: 1 })).toEqual([])
  expect(minus(lostLines(head, 'a\nc\n'), { b: 1 })).toEqual(['d'])
  expect(minus(['x', 'x', 'y'], ['x'])).toEqual(['x', 'y'])
})

test('an approved loss of a repeated line leaves no loss, where removing it from HEAD would report one', async () => {
  const head = 'A\n})\nB\n})\n'
  const now = 'A\n})\nB\n'
  expect(minus(align(head, now).gone, { '})': 1 })).toEqual([])
  expect(minus(align(head, 'A\nB\n').gone, { '})': 1 })).toEqual(['})'])
})

test('the HEAD-line rule judges only what this edit loses, counting a repeated line', async () => {
  const head = 'x()\nx()\ny()\n'
  expect(findings('test', 'a.test.ts', head, 'x()\ny()\nz()\n', false, ['x()'])).toBeUndefined()
  expect(findings('test', 'a.test.ts', head, 'y()\n', false, ['x()'])?.line).toBe('x()')
  expect(findings('test', 'a.test.ts', head, 'x()\n', false, ['x()'])?.line).toBe('y()')
  expect(findings('test', 'a.test.ts', head, 'x()\n', false, ['x()'])?.what).toContain('changes or removes')
})

test('an opened path skips the HEAD-line rule and keeps every content rule', async () => {
  const changed = PY.replace('    assert send() == 1', '    assert send() == 2')
  expect(findings('test', 'test_a.py', PY, changed, true)).toBeUndefined()
  expect(findings('test', 'test_a.py', PY, changed)?.what).toContain('changes or removes')
  expect(findings('test', 'test_a.py', PY, changed.replace('def test_mute', '@pytest.mark.skip\ndef test_mute'), true)?.what).toContain('skips the HEAD test `def test_mute():`')
  expect(findings('test', 'test_a.py', PY, `${changed}\nsys.exit(0)\n`, true)?.what).toContain('exits the test process')
  const ci = 'jobs:\n  test:\n    steps:\n      - run: npm test\n'
  expect(findings('config', '.github/workflows/ci.yml', ci, ci.replace('npm test', 'npm test || true'), true)?.what).toContain('stops tests from running')
  expect(findings('test', 'test_a.py', PY, PY.replace('def test_sends():\n    assert send() == 1\n', ''), true)).toBeUndefined()
})

test('a skip marker below a lost line still applies to its HEAD test', async () => {
  const next = PY.replace('    assert send() == 1', '    assert send() == 2').replace('def test_mute', '@pytest.mark.skip\ndef test_mute')
  expect(findings('test', 'test_a.py', PY, next, true)?.what).toContain('skips the HEAD test')
})

const WF = 'jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v3\n      - uses: pnpm/action-setup@a3252b78c470c02df07e9d59298aecedc3ccdd6d # v3.0.0\n      - run: npm test\n'
test('a workflow step that only changes its action ref keeps the HEAD line', async () => {
  pass('config', '.github/workflows/ci.yml', WF, WF.replace('checkout@v3', 'checkout@v4'))
  pass('config', '.github/workflows/ci.yml', WF, WF.replace('@a3252b78c470c02df07e9d59298aecedc3ccdd6d # v3.0.0', '@fe02b34f77f8bc703788d5817da081398fad5dd2 # v4.0.0'))
  pass('config', '/repo/.github/workflows/ci.yml', WF, WF.replace('checkout@v3', 'checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2'))
})

test('a workflow step with a new action name, or a removed step, is refused; a ref change outside workflows is refused', async () => {
  deny('config', '.github/workflows/ci.yml', WF, WF.replace('actions/checkout@v3', 'evil/checkout@v3'), 'changes or removes a line')
  deny('config', '.github/workflows/ci.yml', WF, WF.replace('      - uses: actions/checkout@v3\n', ''), 'changes or removes a line')
  deny('config', '.pre-commit-config.yaml', WF, WF.replace('checkout@v3', 'checkout@v4'), 'changes or removes a line')
  deny('config', '.husky/pre-commit', WF, WF.replace('checkout@v3', 'checkout@v4'), 'changes or removes a line')
})
