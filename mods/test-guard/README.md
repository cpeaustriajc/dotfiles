# test-guard

A mod (a plugin that adds a hook to Claude Code) that stops Claude from passing a failing test by changing the test or runner. Claude can add tests, but you approve each change to a line that a test file has at `HEAD`.

## Why

An agent with a red test sometimes games it instead of fixing the code (reward hacking). It turns `toHaveBeenCalledTimes(1)` into `toHaveBeenCalled()`, skips the test, or patches the pytest report. The test goes green while the bug stays.

test-guard shows you that edit with the line it changes, and you approve or refuse it. When you ask for a behaviour change, approve the new expected value. When nobody can approve, the edit is refused.

## Install

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install test-guard@dotfiles
```

To see that it is on, run `claude plugin list` and look for `test-guard`. The mod is optional. `dotfiles` does not install it.

## Example

1. A test fails, and Claude edits `tests/notify.test.ts` to change `toHaveBeenCalledTimes(1)` to `toHaveBeenCalled()`.
2. The hook reads the file at `HEAD` with `git show` and finds that the old line is gone.
3. The approval dialog shows: "test-guard: this edit changes or removes a line that tests/notify.test.ts has at HEAD".
4. Approve it if you asked for this behaviour to change. Otherwise refuse it, and Claude fixes the code.
5. After a yes, Claude can change existing lines of that file until the turn ends.
6. To let Claude change the file for the rest of the session with no dialog, run `/test-guard allow tests/notify.test.ts`.

## What it does

The hook checks every Edit, MultiEdit and Write to a guarded file at `tool.check`, the permission decision:

- A test file: `*.test.*`, `*.spec.*`, `test_*.py`, `test_*.sh`, `*_test.py`, `*_test.go`, `conftest.py`, `*.snap` or `*.golden`.
- A file in a `test`, `tests`, `__tests__`, `e2e`, `__snapshots__` or `testdata` folder.
- Runner and CI config: `jest`, `vitest` and `playwright` config files, `pytest.ini`, `.pre-commit-config.yaml`, and the `.github/workflows` and `.husky` folders.
- A shared file: `package.json`, `pyproject.toml`, `setup.cfg` or `tox.ini`.

The hook asks git for the path from the repository root, so a project in `~/e2e/demo/` does not make every file a test file.

| Case | Decision |
|---|---|
| The file is not guarded, or the folder has no git repository or commit | Pass. |
| A test or config file keeps every non-blank `HEAD` line, in the same order | Pass. |
| A `HEAD` line of a test or config file changes, goes away, or moves into a block comment | Ask. A yes covers that file's `HEAD` lines until the turn ends. |
| A workflow step `uses: <name>@<ref>` gets a new ref or comment, with the same name | Pass. |
| An added skip marker, skip call or bare `return` applies to a `HEAD` test | Ask. On a new test it passes. |
| A test file with `HEAD` tests gets `.only`, `describe.skip`, `pytestmark` skip, `@ts-nocheck` or `if (false)` | Ask. |
| A file with a test name gets `sys.exit(0)`, `raise SystemExit` (bare, `()`, `(0)` or `(None)`), `exit()`, `quit()`, `os._exit(0)`, `process.exit()` or `pytest.exit` | Ask, in a new file too. |
| A test file sets a report `outcome` to passed, clears `longrepr`, or patches `TestReport` | Ask, in a new file too. |
| A test file adds `__eq__` that returns `True`, or `asymmetricMatch` that returns `true` | Ask, in a new file too. |
| A tracked config or shared file holds more `passWithNoTests`, `--deselect` or `continue-on-error: true` than at `HEAD` | Ask. Config also asks for `\|\| true`. |
| You ran `/test-guard allow <path>` for this file in this session | Pass. |
| A finding where nobody can approve, such as a background subagent | Deny. Claude reads the line and one next step. |
| `git show` fails for another reason, or the hook fails | Fail closed. Deny with "could not check". |
| A turn ends, and a `HEAD` line of a tracked test or config file is gone, not by an approved edit | Block the stop once and write a log line. |

The dialog names the file and the line. Each content rule (skip, exit, report, equality, pass-anyway flag) asks for each edit, in an approved file too. A deny tells Claude to fix the code, or to stop and tell you which test is wrong and why.

The turn check covers changes that Bash, an MCP tool or a subagent made. At the start of each turn, the hook notes `HEAD` and the lines already gone, so your own edits are not blamed on Claude.

`/test-guard allow <path>` allows one file until the session ends. `/test-guard` alone lists the allowed files. The hook takes `allow` only when you type it. A model, a peer session or a coordinator gets a refusal.

## Settings

No settings and no allow list file.

To turn the mod off, run `claude plugin disable test-guard@dotfiles`.

## Limits

- It never asks about Bash, because Claude Code decides Bash. A `sed -i`, `rm` or `jest -u` runs, and the turn check reports it at the turn's end.
- The turn check compares with the `HEAD` of the turn's start. A weaker test committed in an earlier turn passes; the base-branch check and CI must catch that.
- A `git pull` in a turn can report lines that other people removed.
- An approved file is not checked at the turn's end, so a Bash change to it in the same turn passes.
- The kit that runs the tests cannot play a person who approves, so the approved path is tested in parts.
- Content rules match plain text. A skip under another name, an exit with another code, or a wildcard object passes.
- A hardcoded result in a source file passes. Property tests and mutation testing must catch that.
- The comment scanner reads quotes and comments, not regular expressions. A regular expression that holds `/*` or a backtick can cause a false deny.
- A `fixtures` folder outside a test folder is not guarded.
- A moved line or a changed indent counts as a change and gets an ask.
- A host program or a `PermissionRequest` hook that approves every ask also approves these edits.
- A plugin with a `tool.check` hook above this mod can answer over it.
- The mod is always on. It is not the "careful mode" that `SCOPE.md` rejects, which runs hooks only while a skill runs.
- The edit check fails closed: retry, or allow the file. The turn check fails open, and writes a debug log line.

## More

- [hooks/register.ts](hooks/register.ts): the hooks. [hooks/check.ts](hooks/check.ts): the guarded paths and the rules.
- [hooks/register.test.ts](hooks/register.test.ts), [hooks/check.test.ts](hooks/check.test.ts) and [hooks/turn.test.ts](hooks/turn.test.ts): the tests, with seeded property tests.
- [marketplace.json](../../.claude-plugin/marketplace.json): the manifest, in this mod's entry.
- [nizos/tdd-guard](https://github.com/nizos/tdd-guard): the prior art. It blocks code without a failing test and asks a model; test-guard protects old test lines with a fixed check.
- [ImpossibleBench](https://arxiv.org/abs/2510.20270) and [MacDiarmid et al.](https://arxiv.org/abs/2511.18397): the cheats the content rules name.
