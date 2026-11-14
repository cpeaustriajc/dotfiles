# test-guard

A mod (a plugin that adds a hook to Claude Code) that stops Claude from passing a failing test by changing the test or runner. A small model picks its rules for each project, from that project's own history.

## Why

An agent with a red test sometimes games it instead of fixing the code (reward hacking). It turns `toHaveBeenCalledTimes(1)` into `toHaveBeenCalled()`, skips the test, or patches the pytest report. The test goes green while the bug stays.

test-guard shows you that edit with the line it changes, and you approve or refuse it. When nobody can approve, the edit is refused. Projects differ: in some, most honest commits change test lines, so the model picks the rules from the history.

## Install

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install test-guard@dotfiles
```

The first session in each project sets it up. The hook replays the history, Haiku picks the rules from the counts, and a toast names the pick. The mod is optional. `dotfiles` does not install it.

## Example

1. Start a session in a project that has no rules yet.
2. The hook replays the last 200 commits: for example, 57 test file changes, 31 full-rule asks and 1 rig-rule ask.
3. Haiku gets the rule sets and those counts, with no text from the repository. It answers `rigs`, `full` or `off`.
4. A toast says `test-guard: rig rules only in <repo>, picked by the model.` with the counts.
5. Later, Claude edits `tests/test_notify.py` to add `@pytest.mark.skip` above a test that `HEAD` has.
6. The approval dialog names the file and the line. Refuse it, and Claude fixes the code.

## What it does

The hook checks every Edit, MultiEdit and Write to a guarded file at `tool.check`, the permission decision. A guarded file is a test file: `*.test.*`, `*.spec.*`, `test_*.py`, `test_*.sh`, `*_test.py`, `*_test.go`, `conftest.py`, `*.snap` or `*.golden`. A file in a `test`, `tests`, `__tests__`, `e2e`, `__snapshots__` or `testdata` folder is a test file too. It is also runner and CI config (`jest`, `vitest` and `playwright` config, `pytest.ini`, `.pre-commit-config.yaml`, `.github/workflows`, `.husky`), or a shared file (`package.json`, `pyproject.toml`, `setup.cfg`, `tox.ini`).

| Mode | What runs |
|---|---|
| Not set up, or `Off` | Nothing. Every edit gets the decision that Claude Code gives. |
| `Rig rules only` | The content rules: skip, exit, report, equality and pass-anyway flag. |
| `Full rules` | The content rules, the `HEAD`-line rule and the turn check. |

| Case | Decision |
|---|---|
| The file is not guarded, or the folder has no git repository or commit | Pass. |
| A `HEAD` line of a test or config file changes, goes away, or moves into a block comment (full rules) | Ask. A yes covers that file's `HEAD` lines until the turn ends. |
| A workflow step `uses: <name>@<ref>` gets a new ref or comment, with the same name | Pass. |
| An added skip marker, skip call or bare `return` applies to a `HEAD` test | Ask. On a new test it passes. |
| A test file with `HEAD` tests gets `.only`, `describe.skip`, `pytestmark` skip, `@ts-nocheck` or `if (false)` | Ask. |
| A file with a test name gets `sys.exit(0)`, `raise SystemExit`, `exit()`, `quit()`, `os._exit(0)`, `process.exit()` or `pytest.exit` | Ask, in a new file too. |
| A test file sets a report `outcome` to passed, clears `longrepr`, patches `TestReport`, or adds an always-true `__eq__` or `asymmetricMatch` | Ask, in a new file too. |
| A tracked config or shared file holds more `passWithNoTests`, `--deselect` or `continue-on-error: true` than at `HEAD` | Ask. Config also asks for `\|\| true`. |
| You ran `/test-guard allow <path>` for this file in this session | Pass. |
| A finding where nobody can approve, such as a background subagent | Deny. Claude reads the line and one next step. |
| A turn ends, and a `HEAD` line of a tracked test or config file is gone, not by an approved edit (full rules) | Block the stop once and write a log line. |

The turn check covers changes that Bash, an MCP tool or a subagent made. At the start of each turn, the hook notes `HEAD` and the lines already gone.

`/test-guard` alone shows the mode, the date it was set, who set it, and the allowed files. `/test-guard allow <path>` allows one file until the session ends. The hook takes `setup` and `allow` only when you type them. The session's own model never picks the rules. A model, a peer session or a coordinator gets a refusal.

## Settings

The choice is stored in the mod's own store, a JSON file under your Claude Code configuration folder. The key is the repository's `origin` remote, or its main working tree when it has no remote, so worktrees share it.

To have the model pick again, run `/test-guard setup`. To choose yourself, run `/test-guard setup rigs`, `/test-guard setup full` or `/test-guard setup off`. If the model call fails or names no rules, nothing is saved, the toast names those three commands, and the next session tries again. To turn the mod off everywhere, run `claude plugin disable test-guard@dotfiles`.

## Limits

- The replay reads commits, which are coarser than an agent's edits. It stops at 300 guarded file changes and says so (`COMMITS` and `CAP` in `hooks/register.ts`).
- A profile is per repository, not per branch.
- The replay runs when the first session in a project starts, so that start can take seconds in a large history.
- The pick is one Haiku call, billed to the session's credentials.
- Anyone who can write your Claude Code configuration folder can change the choice. The agent that the mod guards must not have write access there.
- If the store cannot be read, the hook passes that call and writes a debug log line.
- It never asks about Bash, because Claude Code decides Bash. A `sed -i`, `rm` or `jest -u` runs, and the turn check reports it.
- The turn check compares with the `HEAD` of the turn's start. A weaker test committed in an earlier turn passes; CI must catch that.
- A `git pull` in a turn can report lines that other people removed. An approved file is not checked at the turn's end.
- Content rules match plain text. A skip under another name, an exit with another code, or a hardcoded result in a source file passes.
- The comment scanner reads quotes and comments, not regular expressions. A regular expression that holds `/*` or a backtick can cause a false deny.
- A moved line or a changed indent counts as a change and gets an ask.
- A host program or a `PermissionRequest` hook that approves every ask also approves these edits. A plugin with a `tool.check` hook above this mod can answer over it.
- The kit that runs the tests cannot play a person who approves, so the approved path is tested in parts.
- The edit check fails closed: retry, or allow the file. The turn check fails open, and writes a debug log line.

## More

- [hooks/register.ts](hooks/register.ts): the hooks, the profile and the setup replay. [hooks/check.ts](hooks/check.ts): the guarded paths and the rules.
- [hooks/register.test.ts](hooks/register.test.ts), [hooks/check.test.ts](hooks/check.test.ts), [hooks/turn.test.ts](hooks/turn.test.ts) and [hooks/setup.test.ts](hooks/setup.test.ts): the tests.
- [marketplace.json](../../.claude-plugin/marketplace.json): the manifest, in this mod's entry.
