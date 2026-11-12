// The pure part of test-guard: which files it guards, and what an edit to one may not do.

// `test`: the HEAD-line rule and the content rules. `config`: runner and CI config, the HEAD-line rule
// and CONFIG_ADD. `shared`: files that also hold other settings, CONFIG_ADD only.
export type Kind = 'test' | 'config' | 'shared'
export type Change = { old_string: string; new_string: string; replace_all?: boolean }
// `lost`: the HEAD-line rule found it; else a content rule (a rig).
export type Finding = { what: string; line: string; lost?: true }

// Kept the same as TEST_NAME and TEST_DIR in review-loop's tests_kept.py; scripts/check_test_names.py fails on drift.
const TEST_NAME = [/\.(test|spec)\.[^/]+$/, /(^|\/)test_[^/]*\.(py|sh)$/, /_test\.(py|go)$/, /(^|\/)conftest\.py$/, /\.(snap|golden)$/]
const TEST_DIR = new Set(['test', 'tests', '__tests__', 'e2e', '__snapshots__', 'testdata'])
// A removed exclude line or a dropped test step makes the suite skip tests and stay green.
const CONFIG_NAME = /(^|\/)((jest|vitest|playwright)\.config\.[^/]+|vitest\.workspace\.[^/]+|pytest\.ini|\.pre-commit-config\.ya?ml)$/
const CONFIG_DIR = /^(\.github\/workflows|\.husky)\//
const SHARED_NAME = /(^|\/)(package\.json|pyproject\.toml|setup\.cfg|tox\.ini)$/

const slash = (p: string) => p.replace(/\\/g, '/')
const inTestDir = (p: string) => p.split('/').slice(0, -1).some(s => TEST_DIR.has(s))

// The kind a name alone gives, with no git: a test name or a runner config name.
export function nameKind(path: string): Kind | undefined {
  const p = slash(path)
  if (TEST_NAME.some(re => re.test(p))) return 'test'
  if (CONFIG_NAME.test(p)) return 'config'
  return undefined
}

// The kind of a path from the repository root.
export function kindOf(rel: string): Kind | undefined {
  const p = slash(rel)
  const k = nameKind(p)
  if (k) return k
  if (inTestDir(p)) return 'test'
  if (CONFIG_DIR.test(p)) return 'config'
  return SHARED_NAME.test(p) ? 'shared' : undefined
}

// A quick test on the absolute path: false means no kind, so no git runs.
export const maybeGuarded = (path: string) => {
  const p = slash(path)
  return nameKind(p) !== undefined || inTestDir(p) || /\/(\.github\/workflows|\.husky)\//.test(p) || SHARED_NAME.test(p)
}

export function apply(text: string, c: Change): string {
  if (typeof c.old_string !== 'string' || typeof c.new_string !== 'string') throw new Error('edit without old_string or new_string')
  return c.replace_all ? text.split(c.old_string).join(c.new_string) : text.replace(c.old_string, () => c.new_string)
}

type Lang = 'c' | 'py' | undefined
const langOf = (path: string): Lang =>
  /\.(m?[jt]sx?|c[jt]s|go|java|kts?|scala|swift|rs|c|cc|cpp|h|hpp|cs|dart)$/.test(path) ? 'c' : /\.py$/.test(path) ? 'py' : undefined

// For each line: does it start inside a block comment or a string that spans lines? Quotes that
// end at the line end are skipped so that `'**/*.ts'` opens no comment.
export function hidden(lines: string[], lang: Lang): boolean[] {
  if (!lang) return lines.map(() => false)
  let open = ''
  return lines.map(line => {
    const starts = open !== ''
    for (let i = 0; i < line.length; i++) {
      if (open) {
        if (line[i] === '\\' && open !== '*/') i++
        else if (line.startsWith(open, i)) (i += open.length - 1), (open = '')
        continue
      }
      const two = line.slice(i, i + 2)
      const three = line.slice(i, i + 3)
      if (lang === 'c' && two === '//') break
      if (lang === 'py' && line[i] === '#') break
      if (lang === 'c' && two === '/*') (open = '*/'), i++
      else if (lang === 'c' && line[i] === '`') open = '`'
      else if (lang === 'py' && (three === '"""' || three === "'''")) (open = three), (i += 2)
      else if (line[i] === '"' || line[i] === "'") {
        const q = line[i]
        for (i++; i < line.length && line[i] !== q; i++) if (line[i] === '\\') i++
      }
    }
    return starts
  })
}

// A workflow step `uses: <name>@<ref>`, with an optional trailing comment: a new ref keeps the line.
const WORKFLOW = /(^|\/)\.github\/workflows\//
const USES = /^(\s*(?:-\s+)?uses:\s*)([^@\s#]+)@\S+(?:\s+#.*)?$/
function sameStep(a: string, b: string): boolean {
  const x = USES.exec(a)
  const y = USES.exec(b)
  return !!x && !!y && x[1] === y[1] && x[2] === y[2]
}

// Matches each non-blank HEAD line, in order, to a line of the new text with the same text and the
// same comment state. `lost` is the first HEAD line with no match and `gone` every one; `added`
// marks new-text lines that no HEAD line took.
export function align(head: string, next: string, path = '') {
  const lines = next.split(/\r?\n/)
  const lang = langOf(path)
  const nh = hidden(lines, lang)
  const added = lines.map(() => true)
  const h = head.split(/\r?\n/)
  const hh = hidden(h, lang)
  const steps = WORKFLOW.test(path.replace(/\\/g, '/'))
  const same = (a: string, b: string) => a === b || (steps && sameStep(a, b))
  const gone: string[] = []
  let commented = false
  let at = 0
  for (const [i, line] of h.entries()) {
    if (!line.trim()) continue
    let j = at
    while (j < lines.length && !(same(line, lines[j] as string) && nh[j] === hh[i])) j++
    if (j < lines.length) {
      added[j] = false
      at = j + 1
      continue
    }
    if (!gone.length) commented = !hh[i] && lines.some((l, k) => l === line && nh[k])
    gone.push(line)
  }
  return { lost: gone[0], gone, commented, added, lines }
}

// Every non-blank HEAD line with no match in the new text, in order.
export const lostLines = (head: string, next: string, path = '') => align(head, next, path).gone

// `lines` with `take` taken out, each line as many times as `take` holds it.
export function minus(lines: string[], take: string[] | Record<string, number> = []): string[] {
  const left: Record<string, number> = Array.isArray(take) ? {} : { ...take }
  if (Array.isArray(take)) for (const l of take) left[l] = (left[l] ?? 0) + 1
  return lines.filter(l => !(left[l]! > 0 && left[l]!--))
}

export const firstLost = (head: string, next: string, path = '') => align(head, next, path).lost

const SKIP_DECORATOR = /^\s*@(pytest\.mark\.(skip|skipif|xfail)|unittest\.(skip|skipIf|skipUnless|expectedFailure))\b/
const SKIP_CALL = /\b(pytest\.(skip|xfail)|self\.skipTest|t\.Skip(Now|f)?|ctx\.skip)\s*\(|^\s*return;?\s*$/
const DEF = /^\s*((async\s+)?def|class)\s/
const OPENER = /^\s*((async\s+)?def|class|func)\s|\bfunction\b|=>\s*\{\s*$/
const HEADER = /^\s*((async\s+)?def\s+test|class\s+Test|func\s+Test|(it|test)\s*\()/
// Each skips or focuses the tests of the whole file or block, or turns type checks off.
const FILE_SKIP =
  /\b(describe|context|suite|it|test)\.only\b|\b(fit|fdescribe|ftest|xdescribe)\s*\(|\b(describe|context|suite)\.skip\b|^\s*pytestmark\s*=.*\b(skip|skipif|xfail)\b|@ts-nocheck|^\s*if\s*\(\s*(false|0)\s*\)|^\s*if\s+(False|0)\s*:/
const EXIT = /\b(sys\.exit|os\._exit|process\.exit|os\.Exit)\s*\(\s*0?\s*\)|\bpytest\.exit\s*\(/
// The pytest report patch (MacDiarmid et al.): set `outcome` to passed and clear `longrepr`.
const REPORT = /\.outcome\s*=\s*['"](passed|skipped)['"]|\b(rep|report)\.(outcome|longrepr)\s*=(?!=)|\blongrepr\s*=\s*None\b|\bTestReport\.\w+\s*=(?!=)|\bsetattr\s*\(\s*TestReport\b/
// Python only, at statement position, so a string or a call such as `raise SystemExit(main())` is not one.
const PY_EXIT = /(?:^|;)\s*(?:raise\s+SystemExit(?:\s*\(\s*(?:0|None)?\s*\))?|(?:exit|quit)\s*\(\s*0?\s*\))\s*(?:;|#.*)?$/
const EQ_LINE =
  /__eq__.*\breturn\s+True\b|__eq__\s*=\s*lambda[^:]*:\s*True\b|__ne__.*\breturn\s+False\b|asymmetricMatch.*\breturn\s+true\b|asymmetricMatch\s*[:=]\s*\([^)]*\)\s*=>\s*true\b/
const EQ_DEF = /\b(def\s+__eq__|asymmetricMatch)\s*\(/
const EQ_RETURN = /^\s*return\s+(True|true);?\s*$/
// Each counts as added only when the file holds more of it than at HEAD, so a line that keeps one can change.
const CONFIG_ADD = [/passWithNoTests/g, /--deselect\b/g, /continue-on-error:\s*true\b/g]
const CONFIG_ONLY_ADD = [/\|\|\s*(true|exit\s+0)\b/g]
const count = (re: RegExp, text: string) => text.match(re)?.length ?? 0

// The test an added line sits in: the nearest function opener above it, if that opener is a test
// header that HEAD has.
function headTest(lines: string[], added: boolean[], i: number): string | undefined {
  for (let j = i - 1; j >= 0; j--) {
    const l = lines[j] ?? ''
    if (OPENER.test(l)) return HEADER.test(l) && !added[j] ? l : undefined
  }
  return undefined
}

// The definition a decorator at i applies to, if HEAD has it and it is a test.
function decorated(lines: string[], added: boolean[], i: number): string | undefined {
  for (let j = i + 1; j < lines.length; j++) {
    const l = lines[j] ?? ''
    if (DEF.test(l)) return HEADER.test(l) && !added[j] ? l : undefined
  }
  return undefined
}

const prevCode = (lines: string[], i: number) => lines.slice(0, i).reverse().find(l => l.trim()) ?? ''

// What an edit that turns `head` (undefined for a new file) into `next` may not do to a file of `kind`.
// `opened`: a person approved changing this file's HEAD lines for the turn, so only the content rules run.
// `had`: the HEAD lines the file lacked before this edit; the HEAD-line rule judges only the lines this edit loses.
export function findings(kind: Kind, path: string, head: string | undefined, next: string, opened = false, had: string[] = []): Finding | undefined {
  const a = head === undefined ? { gone: [] as string[], commented: false, lines: next.split(/\r?\n/), added: [] as boolean[] } : align(head, next, path)
  const lost = minus(a.gone, had)[0]
  if (lost !== undefined && kind !== 'shared' && !opened)
    return { what: `${a.commented && lost === a.gone[0] ? 'comments out' : 'changes or removes'} a line that ${path} has at HEAD`, line: lost, lost: true }
  const { lines } = a
  const added = head === undefined ? lines.map(() => true) : a.added
  for (const [i, l] of lines.entries()) {
    if (!added[i]) continue
    if (kind !== 'test') {
      const rigs = kind === 'config' ? [...CONFIG_ADD, ...CONFIG_ONLY_ADD] : CONFIG_ADD
      if (head !== undefined && rigs.some(re => count(re, l) && count(re, next) > count(re, head)))
        return { what: `stops tests from running or from failing, in ${path}`, line: l }
      continue
    }
    if (head !== undefined) {
      const t = SKIP_DECORATOR.test(l) ? decorated(lines, added, i) : SKIP_CALL.test(l) ? headTest(lines, added, i) : undefined
      if (t) return { what: `skips the HEAD test \`${t.trim()}\` in ${path}`, line: l }
      if (FILE_SKIP.test(l)) return { what: `skips or focuses tests, or turns off checks, in ${path}, which has tests at HEAD`, line: l }
    }
    // A helper script in a test folder may exit; a test file or conftest.py may not.
    if ((EXIT.test(l) || (path.endsWith('.py') && PY_EXIT.test(l))) && nameKind(path)) return { what: `exits the test process with success in ${path}`, line: l }
    if (REPORT.test(l)) return { what: `rewrites the test report in ${path}`, line: l }
    if (EQ_LINE.test(l) || (EQ_RETURN.test(l) && EQ_DEF.test(prevCode(lines, i))))
      return { what: `adds an equality that is always true in ${path}`, line: l }
  }
  return undefined
}
