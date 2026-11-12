import { atom, read, update } from 'claude-code'
import type { Hook, Register } from 'claude-code'
import type { Level } from '../types'

type Api = Parameters<Hook<'classic.Stop'>>[0]
type Check = { status?: string; conclusion?: string; state?: string }
type Pr = {
  url: string
  state: string
  headRefOid: string
  isDraft: boolean
  autoMergeRequest: unknown
  mergeable: string
  reviewDecision: string
  statusCheckRollup: Check[] | null
}

const MOD = 'implement-gate'
const LEVELS: Level[] = ['commit', 'pr', 'ready', 'merged']
// Each block re-prompts the model. The count starts over when the PR gets a new head commit, so a
// run that keeps pushing fixes is not cut off, and one that is stuck stops after this many.
const MAX_BLOCKS = 3
// A hung gh or git (network, an auth prompt) must not hold the turn's end.
const TIMEOUT_MS = 20_000
const GREEN = new Set(['SUCCESS', 'NEUTRAL', 'SKIPPED'])
const FIELDS = 'url,state,headRefOid,isDraft,autoMergeRequest,mergeable,reviewDecision,statusCheckRollup'
const OFF = 'The user can type /implement-gate off to end the gate.'
// The origins where the user typed the command. A model, a peer session or a coordinator cannot end the gate.
const USER = new Set(['composer', 'bridge', 'sdk'])
const TEXT = 'If those words are only text, such as a commit message, write the text to a file and pass the file.'

const level = atom({ plugin: 'implement-gate', key: 'level' } as const, null as Level | null)
const blocks = atom({ plugin: 'implement-gate', key: 'blocks' } as const, 0)
const head = atom({ plugin: 'implement-gate', key: 'head' } as const, null as string | null)

const rank = (l: Level) => LEVELS.indexOf(l)
const isImplement = (name: string) => name === 'implement' || name.endsWith(':implement')

// Only the last word: "/implement fix the commit hook SHOP-42" must not read as `commit`.
function levelOf(args: string): Level {
  const last = args.trim().toLowerCase().split(/\s+/).pop()?.replace(/[^a-z]+$/, '') ?? ''
  return (LEVELS as string[]).includes(last) ? (last as Level) : 'pr'
}

// The command split at `&&`, `||`, `;`, `|` and line ends, with `\` line breaks joined. Quotes are
// not parsed: a parser of shell text misses forms, and a missed merge passes in silence. Text that
// names a merge is denied instead, which is visible, and the deny says how to get around it.
export const segments = (raw: string) => raw.replace(/\\\r?\n/g, ' ').split(/&&|\|\||;|\||\r?\n/)
const GH = /\bgh\b/
// `merge` as a word, not `merge-base`; and the GraphQL merge mutations.
const MERGE = /\bmerge\b(?!-)|mergePullRequest|enablePullRequestAutoMerge/i
const GRAPHQL_MERGE = /\bgh\s+api\s+graphql\b[\s\S]*\b(mergePullRequest|enablePullRequestAutoMerge)\b/
const PUSH = /\bgit\b.*\bpush\b(.*)/
const CREATE = /\bpr\s+create\b/
// A write to branch protection or a ruleset: the gate rests on them (Transluce saw an agent null the
// required checks, merge, and put them back). A read (no method, no field) passes.
const PROTECTION = /\bgh\s+api\b.*\b(branches\/\S+\/protection|rulesets)\b/
const WRITE = /(-X|--method)[\s=]*['"]?(PUT|PATCH|POST|DELETE)\b|\s(-f|-F|--field|--raw-field|--input)[\s=]/i
const MERGE_TOOL = /merge_pull_request$|merge_merge_request$|auto_?merge/i
const PUSH_TOOL = /push_files$|create_or_update_file$/i

// A default branch named as a push target: `main`, `HEAD:main`, `+refs/heads/main`, `"main"`.
export const targets = (rest: string, b: string) =>
  rest.split(/[\s:+'"=()]+/).some(w => w.replace(/^refs\/heads\//, '') === b)

// A thrown spawn, a timeout and a non-zero exit all come back as an Error that keeps stderr.
async function run($: Api, argv: string[]): Promise<string | Error> {
  try {
    const r = await $.process.run(argv, { cwd: await $.session.cwd(), timeoutMs: TIMEOUT_MS })
    return r.exitCode === 0 ? r.stdout : new Error(r.stderr.trim() || `${argv[0]} exited ${r.exitCode}`)
  } catch (cause) {
    return cause instanceof Error ? cause : new Error(String(cause))
  }
}

async function defaultBranches($: Api): Promise<string[]> {
  const r = await run($, ['git', 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD'])
  return r instanceof Error ? ['main', 'master'] : [r.trim().replace(/^origin\//, '')]
}

async function denial($: Api, raw: string, l: Level): Promise<string | undefined> {
  const below = rank(l) < rank('merged')
  const pushes: string[] = []
  for (const s of segments(raw)) {
    const merging = GH.test(s) && MERGE.test(s)
    if (merging && /--admin\b/.test(s)) return 'bypasses branch protection with --admin'
    if (PROTECTION.test(s) && WRITE.test(s)) return 'changes branch protection or a ruleset'
    if (merging && below && !/--disable-auto\b/.test(s)) return `merges the PR or turns on auto-merge. ${TEXT}`
    const push = PUSH.exec(s)
    if (l === 'commit' && (push || (GH.test(s) && CREATE.test(s)))) return 'pushes or opens a PR'
    if (push) pushes.push(push[1] ?? '')
  }
  if (below && GRAPHQL_MERGE.test(raw)) return `merges the PR or turns on auto-merge. ${TEXT}`
  if (below && pushes.length)
    for (const b of await defaultBranches($)) if (pushes.some(p => targets(p, b))) return `pushes to the default branch ${b}`
  return undefined
}

const running = (c: Check) =>
  (c.status ?? 'COMPLETED') !== 'COMPLETED' || c.state === 'PENDING' || c.state === 'EXPECTED'

function failing(pr: Pr): string | undefined {
  if ((pr.statusCheckRollup ?? []).some(c => !running(c) && !GREEN.has(c.conclusion ?? c.state ?? 'SUCCESS')))
    return `a check failed on ${pr.url}. Fix it and push`
  if (pr.reviewDecision === 'CHANGES_REQUESTED') return `a review requests changes on ${pr.url}`
  if (pr.mergeable === 'CONFLICTING') return `${pr.url} conflicts with its base. Rebase it`
  return undefined
}

function gap(l: Level, pr: Pr | undefined): string | undefined {
  if (!pr) return 'no PR is open for this branch. Open it with create-pr'
  if (pr.state === 'MERGED') return undefined
  if (pr.state !== 'OPEN') return `${pr.url} is ${pr.state.toLowerCase()}. Ask the user with AskUserQuestion`
  if (l === 'pr') return undefined
  if (l === 'ready' && pr.autoMergeRequest) return `auto-merge is on for ${pr.url}. Turn it off with gh pr merge --disable-auto`
  if (pr.isDraft) return `${pr.url} is a draft. Mark it ready with gh pr ready`
  const bad = failing(pr)
  if (bad) return bad
  // Auto-merge waits for running checks itself; `ready` must see them finish.
  if (l === 'merged' && pr.autoMergeRequest) return undefined
  if ((pr.statusCheckRollup ?? []).some(running))
    return `checks are still running on ${pr.url}. Wait in the foreground with gh pr checks --watch (Bash timeout 600000); a waiting command spends no tokens`
  if (l === 'ready') return undefined
  return `the gate holds on ${pr.url}, but auto-merge is off. Turn it on with gh pr merge --auto`
}

async function viewPr($: Api): Promise<Pr | undefined | Error> {
  const r = await run($, ['gh', 'pr', 'view', '--json', FIELDS])
  if (r instanceof Error) return /no pull requests found/i.test(r.message) ? undefined : r
  let pr: Pr
  try {
    pr = JSON.parse(r) as Pr
  } catch (cause) {
    return cause instanceof Error ? cause : new Error(String(cause))
  }
  if (pr.state !== 'MERGED') return pr
  // A merged PR from an earlier use of this branch name is not this run's PR.
  const local = await run($, ['git', 'rev-parse', 'HEAD'])
  return local instanceof Error ? local : local.trim() === pr.headRefOid ? pr : undefined
}

const begin = async ($: Api, l: Level | null) => {
  await update($, level, () => l)
  await update($, blocks, () => 0)
  await update($, head, () => null)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await $.command.register({ name: 'implement-gate', description: 'Show or end the stop point gate of the /implement run', argumentHint: 'off' })
    return result
  })

  on('command.run', { command: 'implement-gate' }, async ($, e) => {
    if (e.args.trim() === 'off') {
      if (e.origin && !USER.has(e.origin.kind)) return { text: `${MOD}: only the user can end the gate, by typing /implement-gate off at the prompt.` }
      await begin($, null)
      return { text: 'The gate is off until the next /implement.' }
    }
    const l = await read($, level)
    return { text: l ? `Stop point: ${l}. Type /implement-gate off to end the gate.` : 'No /implement run is gated.' }
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command && isImplement(e.command.name)) {
      const l = levelOf(e.command.args)
      await begin($, l)
      $.ui.toast(`${MOD}: stop point ${l}`)
    }
    return next(e)
  })

  // The user interrupted the run, so they are back: the gate must not hold their next ask.
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    if (e.agentId === undefined && e.isAborted && (await read($, level))) await begin($, null)
    return result
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const raw = String((e as { command?: unknown }).command ?? '')
    const l = await read($, level)
    if (!l || !/\b(gh|git)\b/.test(raw)) return next(e)
    const why = await denial($, raw, l)
    return why ? { deny: `${MOD}: this command ${why}, past the stop point \`${l}\` that the user typed for /implement. ${OFF}` } : next(e)
  }).catch(($, e, next) =>
    next.called ? next(e) : { deny: `${MOD}: could not check this command (${next.error.message}). Retry it. ${OFF}` },
  )

  // A merge or a push through an MCP server, such as a GitHub server's tools.
  on('tool.call', async ($, e, next) => {
    if (!e.tool.startsWith('mcp__')) return next(e)
    const l = await read($, level)
    if (l && rank(l) < rank('merged') && MERGE_TOOL.test(e.tool)) return { deny: `${MOD}: ${e.tool} merges past the stop point \`${l}\`. ${OFF}` }
    if (l === 'commit' && PUSH_TOOL.test(e.tool)) return { deny: `${MOD}: ${e.tool} pushes past the stop point \`commit\`. ${OFF}` }
    return next(e)
  }).catch(($, e, next) => (next.called ? next(e) : { deny: `${MOD}: could not check ${e.tool} (${next.error.message}). ${OFF}` }))

  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    if (result.block !== undefined || result.preventContinuation) return result
    const l = await read($, level)
    if (!l) return result
    const done = async () => (await begin($, null), result)
    // A git or gh error lets this stop through and keeps the gate for the next one.
    const failed = (why: string) => ($.ui.log(`${MOD}: ${why}; this stop is not checked. ${OFF}`), result)
    if (l === 'commit') return done()
    const [b, main] = await Promise.all([run($, ['git', 'branch', '--show-current']), defaultBranches($)])
    if (b instanceof Error) return failed(`could not read the branch (${b.message})`)
    // On the default branch or a detached HEAD there is no PR to check: a coordinator run, or a
    // repo that opens none.
    if (!b.trim() || main.includes(b.trim())) return done()
    const pr = await viewPr($)
    if (pr instanceof Error) return failed(`could not read the PR (${pr.message})`)
    const why = gap(l, pr)
    if (!why) return done()
    const sha = pr?.headRefOid ?? null
    if (sha !== (await read($, head))) {
      await update($, head, () => sha)
      await update($, blocks, () => 0)
    }
    const n = await read($, blocks)
    if (n >= MAX_BLOCKS) {
      // Keep the gate's denies; only stop blocking, and say so once.
      if (n === MAX_BLOCKS) $.ui.log(`${MOD}: stopped before \`${l}\` after ${MAX_BLOCKS} blocks: ${why}. ${OFF}`)
      await update($, blocks, () => MAX_BLOCKS + 1)
      return result
    }
    await update($, blocks, c => c + 1)
    return { ...result, block: `${MOD}: /implement was typed with \`${l}\`, and ${why}. If you cannot continue alone, ask with AskUserQuestion. (${n + 1} of ${MAX_BLOCKS})` }
  })
}
