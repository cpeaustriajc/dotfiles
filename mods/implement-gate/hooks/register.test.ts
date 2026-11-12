import { expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

type Run = { exitCode: number; stdout?: string; stderr?: string }

function world(on: On, gh: Run | Error = { exitCode: 0, stdout: '{}' }) {
  const w = {
    ran: [] as unknown[], logs: [] as string[], toasts: [] as string[], gh, ghCalls: 0,
    branch: 'shop-42' as string | Error, localHead: 'abc', originHead: { exitCode: 0, stdout: 'origin/main\n' } as Run,
  }
  on('session.cwd', () => ({ value: '/repo' }) as never)
  on('session.start', (_$, e) => e as never)
  on('command.register', () => ({ value: {} }) as never)
  on('process.run', (_$, e) => {
    const argv = (e as { argv: string[] }).argv
    const ok = (r: Run) => ({ value: { stdout: '', stderr: '', ...r } }) as never
    if (argv[0] === 'git' && argv[1] === 'branch') return w.branch instanceof Error ? ok({ exitCode: 128, stderr: w.branch.message }) : ok({ exitCode: 0, stdout: `${w.branch}\n` })
    if (argv[0] === 'git' && argv[1] === 'rev-parse') return ok({ exitCode: 0, stdout: `${w.localHead}\n` })
    if (argv[0] === 'git') return ok(w.originHead)
    w.ghCalls++
    if (w.gh instanceof Error) throw w.gh
    return ok(w.gh)
  })
  on('ui.log', (_$, e) => (w.logs.push(e.text), { value: undefined }) as never)
  on('ui.toast', (_$, e) => (w.toasts.push((e as { text: string }).text), { value: undefined }) as never)
  on('prompt.submit', (_$, e) => ({ text: e.text }) as never)
  on('tool.call', (_$, e) => (w.ran.push(e), { result: { ok: true } }) as never)
  on('classic.Stop', () => ({}) as never)
  on('turn.complete', () => ({ text: '' }) as never)
  return w
}

const implement = ($: any, args: string, name = 'engineering:implement') =>
  $.prompt.submit({ text: `/${name} ${args}`, command: { name, args } })
const bash = async ($: any, command: string) => (await $.tool.call({ tool: 'Bash', command })).deny as string | undefined
const stop = async ($: any) => (await $.classic.Stop({ session_id: 's', transcript_path: '/t', stop_hook_active: false })).block as string | undefined
const gate = ($: any, args: string) => $.command.run({ command: 'implement-gate', args })
const pr = (o: object) => ({
  exitCode: 0,
  stdout: JSON.stringify({
    url: 'https://github.com/o/r/pull/7', state: 'OPEN', headRefOid: 'abc', isDraft: false, autoMergeRequest: null,
    mergeable: 'MERGEABLE', reviewDecision: '', statusCheckRollup: [{ status: 'COMPLETED', conclusion: 'SUCCESS' }], ...o,
  }),
})
const RUNNING = { statusCheckRollup: [{ status: 'IN_PROGRESS' }] }
const FAILED = { statusCheckRollup: [{ status: 'COMPLETED', conclusion: 'FAILURE' }] }
const AUTO = { autoMergeRequest: { enabledAt: 'x' } }

test('with no /implement run, every command passes and stop is not blocked', async ($, on) => {
  const w = world(on)
  expect(await bash($, 'gh pr merge 7 --squash')).toBeUndefined()
  expect(await stop($)).toBeUndefined()
  expect(w.ghCalls).toBe(0)
})

test('the stop point is the last word only, and a toast names it', async ($, on) => {
  const w = world(on)
  await implement($, 'fix the commit hook SHOP-42')
  expect(await bash($, 'git push -u origin shop-42')).toBeUndefined()
  await implement($, 'SHOP-42 commit.')
  expect(await bash($, 'git push -u origin shop-42')).toContain('pushes or opens a PR')
  await implement($, 'SHOP-42', 'implement')
  expect(await bash($, 'gh pr merge 7')).toContain('merges the PR')
  expect(w.toasts).toEqual(['implement-gate: stop point pr', 'implement-gate: stop point commit', 'implement-gate: stop point pr'])
})

test('below merged, every form of a merge is denied', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  for (const cmd of [
    'gh pr merge 7 --squash',
    'git status && gh pr merge --auto --squash',
    'gh -R o/r pr merge 7',
    'gh --repo o/r pr merge 7',
    '(gh pr merge 7)',
    'gh api -X PUT repos/o/r/pulls/7/merge',
    `gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {}) { clientMutationId } }'`,
    'gh api --method=PUT repos/o/r/pulls/$N/merge',
    'gh pr merge 7 \\\n  --squash',
    `git commit -m "it's done" && gh pr merge 7 && echo "can't"`,
    "git commit -F - <<EOF && gh pr merge 7\nmsg\nEOF",
  ]) expect(await bash($, cmd)).toContain('merges the PR')
  expect(await bash($, 'gh pr merge 7 --disable-auto && gh pr merge 7 --squash')).toContain('merges the PR')
  expect(await bash($, 'gh pr view --json mergeable,autoMergeRequest')).toBeUndefined()
  expect(await bash($, 'gh pr checkout 7 && git merge origin/main')).toBeUndefined()
  expect(await bash($, 'gh pr view 7 && git merge-base HEAD origin/main')).toBeUndefined()
})

test('a push of the run\'s own branch passes, even beside a command that names main', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  expect(await bash($, 'git fetch origin main && git rebase origin/main && git push --force-with-lease')).toBeUndefined()
  expect(await bash($, 'git pull --rebase origin main && git push')).toBeUndefined()
  expect(await bash($, 'git diff main --stat; git push origin shop-42')).toBeUndefined()
})

test('text that names a merge is denied too, with a way around it', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42')
  expect(await bash($, "gh pr create --body 'run gh pr merge when green'")).toContain('write the text to a file')
  expect(await bash($, 'gh pr create --body-file body.md')).toBeUndefined()
})

test('a push to the default branch from origin/HEAD is denied below merged', async ($, on) => {
  const w = world(on)
  await implement($, 'SHOP-42')
  for (const cmd of ['git push origin main', 'git push origin HEAD:main', 'git push origin +main', 'git -C /repo push origin refs/heads/main', 'git --no-pager push origin "HEAD:main"'])
    expect(await bash($, cmd)).toContain('default branch main')
  expect(await bash($, 'git push -u origin shop-42')).toBeUndefined()
  expect(await bash($, 'git push origin main-fix')).toBeUndefined()
  w.originHead = { exitCode: 0, stdout: 'origin/develop\n' }
  expect(await bash($, 'git push origin develop')).toContain('default branch develop')
})

test('ready allows turning auto-merge off; merged allows a merge but never --admin', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  expect(await bash($, 'gh pr merge 7 --disable-auto')).toBeUndefined()
  await implement($, 'SHOP-42 merged')
  expect(await bash($, 'gh pr merge 7 --auto --squash')).toBeUndefined()
  expect(await bash($, 'gh pr merge 7 --admin --squash')).toContain('--admin')
  expect(await bash($, 'gh pr merge 7 --squash \\\n  --admin')).toContain('--admin')
})

test('an MCP merge tool is denied below merged', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  expect((await $.tool.call({ tool: 'mcp__github__merge_pull_request', pullNumber: 7 })).deny).toContain('merges past the stop point')
  expect((await $.tool.call({ tool: 'mcp__github__get_pull_request', pullNumber: 7 })).deny).toBeUndefined()
  expect((await $.tool.call({ tool: 'mcp__gitlab__create_merge_request' })).deny).toBeUndefined()
  expect((await $.tool.call({ tool: 'mcp__gitlab__merge_merge_request' })).deny).toContain('merges past')
  await implement($, 'SHOP-42 commit')
  expect((await $.tool.call({ tool: 'mcp__github__push_files' })).deny).toContain('pushes past')
  await implement($, 'SHOP-42 merged')
  expect((await $.tool.call({ tool: 'mcp__github__merge_pull_request', pullNumber: 7 })).deny).toBeUndefined()
})

test('a later prompt keeps the gate; /implement-gate off ends it', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42')
  await $.prompt.submit({ text: 'ok merge it' })
  expect(await bash($, 'gh pr merge 7')).toContain('/implement-gate off')
  expect((await gate($, '')).text).toContain('Stop point: pr')
  await gate($, 'off')
  expect(await bash($, 'gh pr merge 7')).toBeUndefined()
})

test('commit ends the run at the first stop without asking gh', async ($, on) => {
  const w = world(on)
  await implement($, 'SHOP-42 commit')
  expect(await stop($)).toBeUndefined()
  expect(await bash($, 'git push -u origin shop-42')).toBeUndefined()
  expect(w.ghCalls).toBe(0)
})

test('pr blocks stop until a PR is open, then ends the run', async ($, on) => {
  const w = world(on, { exitCode: 1, stderr: 'no pull requests found for branch "shop-42"' })
  await implement($, 'SHOP-42')
  expect(await stop($)).toContain('no PR is open')
  w.gh = pr({})
  expect(await stop($)).toBeUndefined()
  expect(await bash($, 'gh pr merge 7')).toBeUndefined()
})

test('a required check that has not reported counts as running', async ($, on) => {
  world(on, pr({ statusCheckRollup: [{ state: 'EXPECTED' }] }))
  await implement($, 'SHOP-42 ready')
  expect(await stop($)).toContain('still running')
})

test('a detached HEAD is not checked', async ($, on) => {
  const w = world(on)
  w.branch = ''
  await implement($, 'SHOP-42 ready')
  expect(await stop($)).toBeUndefined()
  expect(w.ghCalls).toBe(0)
})

test('on the default branch the stop is not checked', async ($, on) => {
  const w = world(on, { exitCode: 1, stderr: 'no pull requests found' })
  w.branch = 'main'
  await implement($, 'docs/spec.md ready')
  expect(await stop($)).toBeUndefined()
  expect(w.ghCalls).toBe(0)
})

test('ready blocks on a running or failed check, a change request, a conflict or auto-merge', async ($, on) => {
  const w = world(on, pr(RUNNING))
  await implement($, 'SHOP-42 ready')
  expect(await stop($)).toContain('gh pr checks --watch')
  w.gh = pr(FAILED)
  expect(await stop($)).toContain('a check failed')
  w.gh = pr(AUTO)
  expect(await stop($)).toContain('auto-merge is on')
  await implement($, 'SHOP-42 ready')
  w.gh = pr({ reviewDecision: 'CHANGES_REQUESTED' })
  expect(await stop($)).toContain('requests changes')
  w.gh = pr({ mergeable: 'CONFLICTING' })
  expect(await stop($)).toContain('conflicts')
  w.gh = pr({ isDraft: true })
  expect(await stop($)).toContain('draft')
})

test('ready lets stop through once the gate passes', async ($, on) => {
  world(on, pr({}))
  await implement($, 'SHOP-42 ready')
  expect(await stop($)).toBeUndefined()
})

test('merged with auto-merge on waits for running checks but not for a failure', async ($, on) => {
  const w = world(on, pr({}))
  await implement($, 'SHOP-42 merged')
  expect(await stop($)).toContain('gh pr merge --auto')
  w.gh = pr({ ...AUTO, ...FAILED })
  expect(await stop($)).toContain('a check failed')
  w.gh = pr({ ...AUTO, ...RUNNING })
  expect(await stop($)).toBeUndefined()
})

test('stop is blocked at most 3 times per head commit; the denies stay after that', async ($, on) => {
  const w = world(on, pr({ isDraft: true }))
  await implement($, 'SHOP-42 ready')
  for (const n of [1, 2, 3]) expect(await stop($)).toContain(`(${n} of 3)`)
  expect(await stop($)).toBeUndefined()
  expect(await stop($)).toBeUndefined()
  expect(w.logs).toHaveLength(1)
  expect(w.logs[0]).toContain('after 3 blocks')
  expect(await bash($, 'gh pr merge 7')).toContain('merges the PR')
})

test('a new head commit starts the block count over', async ($, on) => {
  const w = world(on, pr(FAILED))
  await implement($, 'SHOP-42 ready')
  for (const n of [1, 2, 3]) expect(await stop($)).toContain(`(${n} of 3)`)
  w.gh = pr({ ...RUNNING, headRefOid: 'def' })
  expect(await stop($)).toContain('(1 of 3)')
})

test('a merged PR from an earlier use of the branch name does not count', async ($, on) => {
  const w = world(on, pr({ state: 'MERGED', headRefOid: 'old' }))
  await implement($, 'SHOP-42')
  expect(await stop($)).toContain('no PR is open')
  w.localHead = 'old'
  expect(await stop($)).toBeUndefined()
})

test('an interrupted run ends the gate', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  await $.turn.complete({ answer: '', durationMs: 1, isAborted: true, reason: 'aborted', turnId: 't' })
  expect(await bash($, 'gh pr merge 7')).toBeUndefined()
})

test('a subagent\'s interrupted turn keeps the gate', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 ready')
  await $.turn.complete({ answer: '', durationMs: 1, isAborted: true, reason: 'aborted', turnId: 't', agentId: 'a1' })
  expect(await bash($, 'gh pr merge 7')).toContain('merges the PR')
})

test('a git or gh error lets that one stop through and keeps the gate', async ($, on) => {
  const w = world(on, { exitCode: 4, stderr: 'gh auth login required' })
  await implement($, 'SHOP-42 ready')
  expect(await stop($)).toBeUndefined()
  expect(await bash($, 'gh pr merge 7')).toContain('merges the PR')
  w.gh = new Error('spawn gh ENOENT')
  expect(await stop($)).toBeUndefined()
  w.gh = { exitCode: 0, stdout: 'warning: x\n{' }
  expect(await stop($)).toBeUndefined()
  w.branch = new Error('not a git repository')
  expect(await stop($)).toBeUndefined()
  expect(w.logs).toHaveLength(4)
  expect(w.logs[3]).toContain('could not read the branch')
  w.branch = 'shop-42'
  w.gh = pr({ isDraft: true })
  expect(await stop($)).toContain('draft')
  expect(w.logs[0]).toContain('gh auth login required')
  expect(w.logs[1]).toContain('could not read the PR')
})

test('a write to branch protection or a ruleset is denied at every stop point; a read passes', async ($, on) => {
  world(on)
  for (const l of ['commit', 'pr', 'ready', 'merged']) {
    await implement($, `SHOP-42 ${l}`)
    for (const cmd of [
      'gh api -X PUT repos/o/r/branches/main/protection --input p.json',
      'gh api --method DELETE repos/o/r/branches/main/protection/required_status_checks',
      'gh api repos/o/r/rulesets/4 -X PATCH -F enforcement=disabled',
      "gh api repos/o/r/branches/main/protection -f 'required_status_checks=null'",
    ]) expect(await bash($, cmd), `${l}: ${cmd}`).toContain('changes branch protection or a ruleset')
    expect(await bash($, 'gh api repos/o/r/branches/main/protection'), l).toBeUndefined()
    expect(await bash($, 'gh api repos/o/r/rulesets --jq .[].name'), l).toBeUndefined()
  }
})

test('/implement-gate off from an origin other than the user keeps the gate', async ($, on) => {
  world(on)
  await implement($, 'SHOP-42 pr')
  for (const kind of ['peer-send-message', 'coordinator', 'plugin', 'unclassified']) {
    const out = await ($ as any).command.run({ command: 'implement-gate', args: 'off', origin: { kind, name: 'x' } })
    expect(out.text).toContain('only the user can end the gate')
  }
  expect(await bash($, 'gh pr merge 7')).toContain('merges the PR')
  await ($ as any).command.run({ command: 'implement-gate', args: 'off', origin: { kind: 'composer' } })
  expect(await bash($, 'gh pr merge 7')).toBeUndefined()
})
