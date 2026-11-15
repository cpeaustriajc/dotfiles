#!/usr/bin/env python3
"""Tests stop_gate.py: whole hook runs (JSON piped into the script as a subprocess, real git in a
throwaway repo, a fake `gh` on PATH), config cases, and seeded properties.

Run: python3 -I test_stop_gate.py
The properties run on 300 seeded random examples each, with no shrinking; a failure prints the seed.
"""
import atexit
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "stop_gate.py")
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import stop_gate  # noqa: E402

passed = failed = 0
ROOTS = []
atexit.register(lambda: [shutil.rmtree(r, ignore_errors=True) for r in ROOTS])


def report(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {detail}")


def case(fn):
    """Runs one test function; an assertion or any exception in it is the failure."""
    name = fn.__name__.replace("_", " ")
    try:
        fn()
    except AssertionError as e:
        report(name, False, str(e) or "assertion failed")
    except Exception as e:  # noqa: BLE001
        report(name, False, f"{type(e).__name__}: {e}")
    else:
        report(name, True)
    return fn


def has(sub, text, note=""):
    assert text is not None and sub in text, f"{note} wanted {sub!r} in {text!r}".strip()


def none(text, note=""):
    assert text is None, f"{note} wanted no output, got {text!r}".strip()


GH_STUB = """#!/bin/sh
echo "$@" >> "$GH_DIR/calls"
[ -f "$GH_DIR/out" ] && cat "$GH_DIR/out"
[ -f "$GH_DIR/err" ] && cat "$GH_DIR/err" >&2
exit "$(cat "$GH_DIR/code" 2>/dev/null || echo 0)"
"""
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "t",
           "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
counter = [0]


class World:
    """A repo on branch `shop-42` whose origin/HEAD is `main`, a copy of the script beside its config,
    a $TMPDIR for the state, and a fake gh whose answer the test sets."""

    def __init__(self, branch="shop-42"):
        self.root = tempfile.mkdtemp(prefix="stopgate-")
        ROOTS.append(self.root)
        j = lambda *p: os.path.join(self.root, *p)  # noqa: E731
        self.repo, self.hooks, self.tmp, self.bin, self.ghdir = j("repo"), j("repo", ".claude", "hooks"), j("tmp"), j("bin"), j("gh")
        for d in (self.hooks, self.tmp, self.bin, self.ghdir):
            os.makedirs(d)
        shutil.copy(SCRIPT, self.hooks)
        self.script = os.path.join(self.hooks, "stop_gate.py")
        with open(os.path.join(self.bin, "gh"), "w") as f:
            f.write(GH_STUB)
        os.chmod(os.path.join(self.bin, "gh"), 0o755)
        self.git("init", "-q", "-b", "main")
        self.git("commit", "-q", "--allow-empty", "-m", "first")
        self.origin("main")
        if branch != "main":
            self.git("checkout", "-q", "-b", branch) if branch else self.git("checkout", "-q", "--detach")
        counter[0] += 1
        self.sid = f"s{counter[0]}"
        self.msgs = []
        self.out = None
        self.gh({})

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
                              env={**os.environ, **GIT_ENV}).stdout.strip()

    def origin(self, name):
        self.git("update-ref", f"refs/remotes/origin/{name}", "HEAD")
        self.git("symbolic-ref", "refs/remotes/origin/HEAD", f"refs/remotes/origin/{name}")

    def head(self):
        return self.git("rev-parse", "HEAD")

    def config(self, cfg):
        with open(os.path.join(self.hooks, "stop_gate.json"), "w") as f:
            f.write(cfg if isinstance(cfg, str) else json.dumps(cfg))

    def gh(self, out="", code=0, err=""):
        """What the fake gh prints and exits with. A dict is printed as JSON."""
        for name, val in (("out", out if isinstance(out, str) else json.dumps(out)), ("err", err), ("code", str(code))):
            with open(os.path.join(self.ghdir, name), "w") as f:
                f.write(val)

    def pr(self, **o):
        self.gh({"url": "https://github.com/o/r/pull/7", "state": "OPEN", "headRefOid": self.head(), "isDraft": False,
                 "autoMergeRequest": None, "mergeable": "MERGEABLE", "reviewDecision": "",
                 "statusCheckRollup": [{"status": "COMPLETED", "conclusion": "SUCCESS"}], **o})

    def ghcalls(self):
        try:
            with open(os.path.join(self.ghdir, "calls")) as f:
                return len(f.read().splitlines())
        except FileNotFoundError:
            return 0

    def hook(self, event, stdin=None, cwd=None, **fields):
        """Pipes one hook event into the script; returns its parsed stdout, or None when it printed nothing."""
        payload = stdin if stdin is not None else json.dumps(
            {"session_id": self.sid, "cwd": cwd or self.repo, "transcript_path": "/t", "hook_event_name": event, **fields})
        env = {**os.environ, **GIT_ENV, "TMPDIR": self.tmp, "GH_DIR": self.ghdir, "CLAUDE_PROJECT_DIR": self.repo,
               "PATH": self.bin + os.pathsep + os.environ["PATH"]}
        r = subprocess.run([sys.executable, "-I", self.script], input=payload, capture_output=True, text=True, env=env, timeout=60)
        assert r.returncode == 0, f"exit {r.returncode}: {r.stderr}"
        self.out = json.loads(r.stdout) if r.stdout.strip() else None
        return self.out

    def prompt(self, text):
        return self.hook("UserPromptSubmit", prompt=text)

    def implement(self, args, name="engineering:implement"):
        return self.prompt(f"/{name} {args}")

    def tool(self, tool, **tool_input):
        """The deny reason, or None when the call passes."""
        out = self.hook("PreToolUse", tool_name=tool, tool_input=tool_input)
        if out is None:
            return None
        h = out["hookSpecificOutput"]
        assert h["hookEventName"] == "PreToolUse" and h["permissionDecision"] == "deny", out
        return h["permissionDecisionReason"]

    def bash(self, command):
        return self.tool("Bash", command=command)

    def stop(self):
        """The block reason, or None. A systemMessage (a log line) goes to self.msgs."""
        out = self.hook("Stop", stop_hook_active=False)
        if out and "systemMessage" in out:
            self.msgs.append(out["systemMessage"])
        if out and out.get("decision") == "block":
            return out["reason"]
        assert out is None or set(out) == {"systemMessage"}, out
        return None

    def gate(self, args=""):
        out = self.hook("UserPromptSubmit", prompt=f"/implement-gate {args}".strip())
        assert out and out["decision"] == "block", out
        return out["reason"]

    def state(self):
        with open(os.path.join(self.tmp, "claude-hooks", self.sid, "stop-gate.json")) as f:
            return json.load(f)


RUNNING = {"statusCheckRollup": [{"status": "IN_PROGRESS"}]}
FAILED = {"statusCheckRollup": [{"status": "COMPLETED", "conclusion": "FAILURE"}]}
AUTO = {"autoMergeRequest": {"enabledAt": "x"}}


# --- hook runs, ported from register.test.ts ---------------------------------------------------

@case
def with_no_implement_run_every_command_passes_and_stop_is_not_blocked():
    w = World()
    none(w.bash("gh pr merge 7 --squash"))
    none(w.stop())
    assert w.ghcalls() == 0


@case
def the_stop_point_is_the_last_word_only_and_the_context_names_it():
    w = World()
    ctx = lambda out: out["hookSpecificOutput"]["additionalContext"]  # noqa: E731
    out = w.implement("fix the commit hook SHOP-42")
    assert out["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    none(w.bash("git push -u origin shop-42"))
    c1 = ctx(out)
    c2 = ctx(w.implement("SHOP-42 commit."))
    has("pushes or opens a PR", w.bash("git push -u origin shop-42"))
    c3 = ctx(w.implement("SHOP-42", name="implement"))
    has("merges the PR", w.bash("gh pr merge 7"))
    assert [c1, c2, c3] == ["implement-gate: stop point pr", "implement-gate: stop point commit", "implement-gate: stop point pr"], (c1, c2, c3)


@case
def below_merged_every_form_of_a_merge_is_denied():
    w = World()
    w.implement("SHOP-42 ready")
    for cmd in [
        "gh pr merge 7 --squash",
        "git status && gh pr merge --auto --squash",
        "gh -R o/r pr merge 7",
        "gh --repo o/r pr merge 7",
        "(gh pr merge 7)",
        "gh api -X PUT repos/o/r/pulls/7/merge",
        "gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {}) { clientMutationId } }'",
        "gh api --method=PUT repos/o/r/pulls/$N/merge",
        "gh pr merge 7 \\\n  --squash",
        "git commit -m \"it's done\" && gh pr merge 7 && echo \"can't\"",
        "git commit -F - <<EOF && gh pr merge 7\nmsg\nEOF",
        "gh pr merge 7 --disable-auto && gh pr merge 7 --squash",
    ]:
        has("merges the PR", w.bash(cmd), cmd)
    none(w.bash("gh pr view --json mergeable,autoMergeRequest"))
    none(w.bash("gh pr checkout 7 && git merge origin/main"))
    none(w.bash("gh pr view 7 && git merge-base HEAD origin/main"))


@case
def a_push_of_the_runs_own_branch_passes_even_beside_a_command_that_names_main():
    w = World()
    w.implement("SHOP-42 ready")
    none(w.bash("git fetch origin main && git rebase origin/main && git push --force-with-lease"))
    none(w.bash("git pull --rebase origin main && git push"))
    none(w.bash("git diff main --stat; git push origin shop-42"))


@case
def text_that_names_a_merge_is_denied_too_with_a_way_around_it():
    w = World()
    w.implement("SHOP-42")
    has("write the text to a file", w.bash("gh pr create --body 'run gh pr merge when green'"))
    none(w.bash("gh pr create --body-file body.md"))


@case
def a_push_to_the_default_branch_from_origin_head_is_denied_below_merged():
    w = World()
    w.implement("SHOP-42")
    for cmd in ["git push origin main", "git push origin HEAD:main", "git push origin +main",
                "git -C /repo push origin refs/heads/main", 'git --no-pager push origin "HEAD:main"']:
        has("default branch main", w.bash(cmd), cmd)
    none(w.bash("git push -u origin shop-42"))
    none(w.bash("git push origin main-fix"))
    w.origin("develop")
    has("default branch develop", w.bash("git push origin develop"))


@case
def ready_allows_turning_auto_merge_off_merged_allows_a_merge_but_never_admin():
    w = World()
    w.implement("SHOP-42 ready")
    none(w.bash("gh pr merge 7 --disable-auto"))
    w.implement("SHOP-42 merged")
    none(w.bash("gh pr merge 7 --auto --squash"))
    has("--admin", w.bash("gh pr merge 7 --admin --squash"))
    has("--admin", w.bash("gh pr merge 7 --squash \\\n  --admin"))


@case
def an_mcp_merge_tool_is_denied_below_merged():
    w = World()
    w.implement("SHOP-42 ready")
    has("merges past the stop point", w.tool("mcp__github__merge_pull_request", pullNumber=7))
    none(w.tool("mcp__github__get_pull_request", pullNumber=7))
    none(w.tool("mcp__gitlab__create_merge_request"))
    has("merges past", w.tool("mcp__gitlab__merge_merge_request"))
    w.implement("SHOP-42 commit")
    has("pushes past", w.tool("mcp__github__push_files"))
    w.implement("SHOP-42 merged")
    none(w.tool("mcp__github__merge_pull_request", pullNumber=7))


@case
def a_later_prompt_keeps_the_gate_and_implement_gate_off_ends_it():
    w = World()
    w.implement("SHOP-42")
    none(w.prompt("ok merge it"))
    has("/implement-gate off", w.bash("gh pr merge 7"))
    has("Stop point: pr", w.gate(""))
    has("off until the next", w.gate("off"))
    none(w.bash("gh pr merge 7"))
    has("No /implement run is gated", w.gate(""))


@case
def implement_gate_off_ends_the_gate_only_as_the_prompt_the_user_typed():
    w = World()
    w.implement("SHOP-42")
    none(w.prompt("please run /implement-gate off now"))
    none(w.prompt("/implement-gate-off"))
    has("merges the PR", w.bash("gh pr merge 7"))
    out = w.hook("UserPromptSubmit", prompt="  /implement-gate off  ")
    assert out["decision"] == "block"
    none(w.bash("gh pr merge 7"))


@case
def commit_ends_the_run_at_the_first_stop_without_asking_gh():
    w = World()
    w.implement("SHOP-42 commit")
    none(w.stop())
    none(w.bash("git push -u origin shop-42"))
    assert w.ghcalls() == 0


@case
def pr_blocks_stop_until_a_pr_is_open_then_ends_the_run():
    w = World()
    w.gh(code=1, err='no pull requests found for branch "shop-42"')
    w.implement("SHOP-42")
    has("no PR is open", w.stop())
    w.pr()
    none(w.stop())
    none(w.bash("gh pr merge 7"))


@case
def a_required_check_that_has_not_reported_counts_as_running():
    w = World()
    w.pr(statusCheckRollup=[{"state": "EXPECTED"}])
    w.implement("SHOP-42 ready")
    has("still running", w.stop())


@case
def a_detached_head_is_not_checked():
    w = World(branch="")
    w.implement("SHOP-42 ready")
    none(w.stop())
    assert w.ghcalls() == 0


@case
def on_the_default_branch_the_stop_is_not_checked():
    w = World(branch="main")
    w.gh(code=1, err="no pull requests found")
    w.implement("docs/spec.md ready")
    none(w.stop())
    assert w.ghcalls() == 0


@case
def ready_blocks_on_a_running_or_failed_check_a_change_request_a_conflict_or_auto_merge():
    w = World()
    w.pr(**RUNNING)
    w.implement("SHOP-42 ready")
    has("gh pr checks --watch", w.stop())
    w.pr(**FAILED)
    has("a check failed", w.stop())
    w.pr(**AUTO)
    has("auto-merge is on", w.stop())
    w.implement("SHOP-42 ready")
    w.pr(reviewDecision="CHANGES_REQUESTED")
    has("requests changes", w.stop())
    w.pr(mergeable="CONFLICTING")
    has("conflicts", w.stop())
    w.pr(isDraft=True)
    has("draft", w.stop())


@case
def ready_lets_stop_through_once_the_gate_passes():
    w = World()
    w.pr()
    w.implement("SHOP-42 ready")
    none(w.stop())


@case
def merged_with_auto_merge_on_waits_for_running_checks_but_not_for_a_failure():
    w = World()
    w.pr()
    w.implement("SHOP-42 merged")
    has("gh pr merge --auto", w.stop())
    w.pr(**AUTO, **FAILED)
    has("a check failed", w.stop())
    w.pr(**AUTO, **RUNNING)
    none(w.stop())


@case
def stop_is_blocked_at_most_3_times_per_head_commit_the_denies_stay_after_that():
    w = World()
    w.pr(isDraft=True)
    w.implement("SHOP-42 ready")
    for n in (1, 2, 3):
        has(f"({n} of 3)", w.stop())
    none(w.stop())
    none(w.stop())
    assert len(w.msgs) == 1, w.msgs
    has("after 3 blocks", w.msgs[0])
    has("merges the PR", w.bash("gh pr merge 7"))


@case
def a_new_head_commit_starts_the_block_count_over():
    w = World()
    w.pr(**FAILED)
    w.implement("SHOP-42 ready")
    for n in (1, 2, 3):
        has(f"({n} of 3)", w.stop())
    w.pr(**RUNNING, headRefOid="def")
    has("(1 of 3)", w.stop())


@case
def a_merged_pr_from_an_earlier_use_of_the_branch_name_does_not_count():
    w = World()
    w.pr(state="MERGED", headRefOid="old")
    w.implement("SHOP-42")
    has("no PR is open", w.stop())
    w.pr(state="MERGED")
    none(w.stop())


@case
def a_git_or_gh_error_lets_that_one_stop_through_and_keeps_the_gate():
    w = World()
    w.gh(code=4, err="gh auth login required")
    w.implement("SHOP-42 ready")
    none(w.stop())
    has("merges the PR", w.bash("gh pr merge 7"))
    w.gh(out="warning: x\n{")
    none(w.stop())
    w.gh(out=json.dumps({"state": 3}))
    none(w.stop())
    outside = tempfile.mkdtemp(prefix="stopgate-nogit-")
    ROOTS.append(outside)
    out = w.hook("Stop", cwd=outside, stop_hook_active=False)
    w.msgs.append(out["systemMessage"])
    assert len(w.msgs) == 4, w.msgs
    has("could not read the branch", w.msgs[3])
    w.pr(isDraft=True)
    has("draft", w.stop())
    has("gh auth login required", w.msgs[0])
    has("could not read the PR", w.msgs[1])
    has("could not read the PR", w.msgs[2])


@case
def a_gh_that_is_missing_or_hangs_comes_back_as_an_error():
    old = stop_gate.TIMEOUT_S
    stop_gate.TIMEOUT_S = 1
    try:
        t = time.time()
        r = stop_gate.run(["sleep", "5"], ".")
        assert isinstance(r, stop_gate.Error) and "took over" in str(r) and time.time() - t < 4, r
        assert isinstance(stop_gate.run(["no-such-gh-binary", "pr"], "."), stop_gate.Error)
        assert stop_gate.run(["echo", "hi"], ".") == "hi\n"
    finally:
        stop_gate.TIMEOUT_S = old
    assert old == 20


@case
def a_write_to_branch_protection_or_a_ruleset_is_denied_at_every_stop_point_a_read_passes():
    w = World()
    for lvl in ("commit", "pr", "ready", "merged"):
        w.implement(f"SHOP-42 {lvl}")
        for cmd in [
            "gh api -X PUT repos/o/r/branches/main/protection --input p.json",
            "gh api --method DELETE repos/o/r/branches/main/protection/required_status_checks",
            "gh api repos/o/r/rulesets/4 -X PATCH -F enforcement=disabled",
            "gh api repos/o/r/branches/main/protection -f 'required_status_checks=null'",
        ]:
            has("changes branch protection or a ruleset", w.bash(cmd), f"{lvl}: {cmd}")
        none(w.bash("gh api repos/o/r/branches/main/protection"), lvl)
        none(w.bash("gh api repos/o/r/rulesets --jq .[].name"), lvl)


# --- fail-closed and fail-open, state, self-protection -----------------------------------------

@case
def a_hook_that_fails_denies_a_bash_call_and_an_mcp_call_but_lets_a_stop_through():
    w = World()
    w.implement("SHOP-42 ready")
    path = os.path.join(w.tmp, "claude-hooks", w.sid, "stop-gate.json")
    with open(path, "w") as f:
        f.write("{not json")
    has("could not check this command", w.bash("gh pr merge 7"))
    has("could not check mcp__github__merge_pull_request", w.tool("mcp__github__merge_pull_request"))
    none(w.stop())
    assert len(w.msgs) == 1 and "could not check this stop" in w.msgs[0], w.msgs
    for event in ("Stop", "PreToolUse", "UserPromptSubmit"):
        none(w.hook(event, stdin="not json"))
        none(w.hook(event, stdin="[1]"))


@case
def the_state_is_a_file_outside_the_tree_keyed_by_the_session():
    w = World()
    w.implement("SHOP-42 ready")
    assert w.state() == {"level": "ready", "blocks": 0, "head": None}
    inside = [p for p in w.git("ls-files", "--others", "--exclude-standard").splitlines() if "stop-gate" in p]
    assert inside == [], inside
    assert not os.path.exists(os.path.join(w.repo, "claude-hooks"))
    other = World()
    other.tmp = w.tmp
    other.sid = "someone-else"
    none(other.bash("gh pr merge 7"))
    w.sid = "../../escape"
    w.implement("SHOP-42")
    dirs = os.listdir(os.path.join(w.tmp, "claude-hooks"))
    assert "_._.._escape" in dirs and not [d for d in dirs if "/" in d], dirs
    assert not os.path.exists(os.path.join(w.tmp, "escape")) and not os.path.exists(os.path.join(w.root, "escape"))


@case
def state_falls_back_to_tmp_when_tmpdir_is_unset():
    old = os.environ.pop("TMPDIR", None)
    try:
        assert stop_gate.state_path("abc") == "/tmp/claude-hooks/abc/stop-gate.json"
    finally:
        if old is not None:
            os.environ["TMPDIR"] = old


@case
def while_gated_the_agent_cannot_edit_the_gates_own_files_or_the_project_settings():
    w = World()
    own = [os.path.join(w.hooks, "stop_gate.py"), os.path.join(w.hooks, "stop_gate.json"),
           os.path.join(w.hooks, "new_file.py"), os.path.join(w.repo, ".claude", "settings.json")]
    for p in own:
        none(w.tool("Edit", file_path=p, old_string="a", new_string="b"), "not gated")
    w.implement("SHOP-42 commit")
    for tool in ("Edit", "Write", "MultiEdit"):
        for p in own:
            has("gate's own files", w.tool(tool, file_path=p), f"{tool} {p}")
    has("gate's own files", w.tool("Write", file_path=".claude/settings.json"))
    has("gate's own files", w.tool("Write", file_path="x/../.claude/hooks/stop_gate.py"))
    none(w.tool("Edit", file_path=os.path.join(w.repo, "src", "app.py")))
    none(w.tool("Write", file_path=os.path.join(w.repo, ".claude", "settings.local.json")))
    none(w.tool("Read", file_path=own[0]))
    w.gate("off")
    none(w.tool("Edit", file_path=own[0]))


# --- config ------------------------------------------------------------------------------------

@case
def config_default_branch_replaces_origin_head():
    w = World()
    w.config({"default_branch": "trunk"})
    w.implement("SHOP-42")
    has("default branch trunk", w.bash("git push origin trunk"))
    none(w.bash("git push origin main"))
    w.git("checkout", "-q", "-b", "trunk")
    w.gh(code=1, err="no pull requests found")
    none(w.stop())
    assert w.ghcalls() == 0


@case
def a_null_default_branch_reads_origin_head_and_falls_back_to_main_and_master():
    w = World()
    w.config({"default_branch": None})
    w.implement("SHOP-42")
    has("default branch main", w.bash("git push origin main"))
    w.git("symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
    has("default branch main", w.bash("git push origin main"))
    has("default branch master", w.bash("git push origin master"))


@case
def config_merge_and_push_tools_replace_the_defaults():
    w = World()
    w.config({"merge_tools": ["Land_Change"], "push_tools": ["ship_it"]})
    w.implement("SHOP-42 ready")
    has("merges past", w.tool("mcp__forge__land_change"))
    none(w.tool("mcp__github__merge_pull_request"))
    w.implement("SHOP-42 commit")
    has("pushes past", w.tool("mcp__forge__ship_it"))
    none(w.tool("mcp__github__push_files"))


@case
def config_max_blocks_sets_the_block_limit():
    w = World()
    w.config({"max_blocks": 1})
    w.pr(isDraft=True)
    w.implement("SHOP-42 ready")
    has("(1 of 1)", w.stop())
    none(w.stop())
    has("after 1 blocks", w.msgs[0])


@case
def a_missing_or_malformed_config_gives_the_defaults():
    w = World()
    for cfg in (None, "{broken", "[1]", {"default_branch": 5, "merge_tools": "x", "push_tools": [1], "max_blocks": -2},
                {"max_blocks": True}, {"default_branch": "  "}):
        if cfg is not None:
            w.config(cfg)
        w.implement("SHOP-42 ready")
        has("merges past", w.tool("mcp__github__merge_pull_request"), repr(cfg))
        has("default branch main", w.bash("git push origin main"), repr(cfg))
    w.pr(isDraft=True)
    for n in (1, 2, 3):
        has(f"({n} of 3)", w.stop())


@case
def the_config_is_read_from_the_folder_of_the_script():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "stop_gate.json")
        with open(p, "w") as f:
            json.dump({"default_branch": "trunk", "max_blocks": 5}, f)
        cfg = stop_gate.load_config(p)
        assert cfg["default_branch"] == "trunk" and cfg["max_blocks"] == 5 and cfg["push_tools"] == stop_gate.DEFAULTS["push_tools"]
    assert stop_gate.HERE == os.path.dirname(os.path.realpath(SCRIPT))


@case
def the_settings_file_wires_all_three_events_to_the_script():
    with open(os.path.join(HERE, "stop_gate.settings.json")) as f:
        s = json.load(f)
    assert set(s) == {"hooks"} and set(s["hooks"]) == {"UserPromptSubmit", "PreToolUse", "Stop"}
    cmd = 'python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/stop_gate.py'
    for event, groups in s["hooks"].items():
        assert [h["command"] for g in groups for h in g["hooks"]] == [cmd], event
    matcher = s["hooks"]["PreToolUse"][0]["matcher"]
    import re
    for t in ("Bash", "Edit", "Write", "MultiEdit", "mcp__github__merge_pull_request"):
        assert re.fullmatch(matcher, t), t


# --- properties (seeded, no shrinking) ---------------------------------------------------------

SEED = int(time.time()) % 2**31
WORDS = ["gh", "pr", "merge", "7", "git", "push", "origin", "main", "echo", "hi", "--squash", "x.txt"]
SEPS = [" && ", " || ", "; ", " | ", "\n"]
BENIGN = ["echo hi", "git status", "ls -la", "git fetch origin main", "gh pr view 7", "git diff main --stat"]


@case
def property_a_command_joined_by_and_or_semicolon_pipe_or_line_end_splits_into_exactly_its_parts():
    r = random.Random(SEED)
    for k in range(300):
        parts = [" ".join(r.choice(WORDS) for _ in range(r.randint(1, 4))) for _ in range(r.randint(1, 5))]
        raw = parts[0]
        for p in parts[1:]:
            raw += r.choice(SEPS) + p
        got = [s.strip() for s in stop_gate.segments(raw)]
        assert got == parts, f"seed {SEED} run {k}: {raw!r} -> {got}"


@case
def property_a_backslash_line_break_never_splits_a_command():
    r = random.Random(SEED + 1)
    for k in range(300):
        raw = " \\\n  ".join(r.choice(WORDS) for _ in range(r.randint(2, 6)))
        assert len(stop_gate.segments(raw)) == 1, f"seed {SEED + 1} run {k}: {raw!r}"


@case
def property_a_branch_is_a_push_target_as_a_whole_word_never_as_part_of_a_longer_name():
    r = random.Random(SEED + 2)
    forms = lambda b: [b, f"HEAD:{b}", f"+refs/heads/{b}", f'"{b}"', f"'{b}'", f"refs/heads/{b}", f"x:{b}"]  # noqa: E731
    for _ in range(300):
        b = r.choice(["main", "master", "trunk", "release/1.2"])
        lead = f" origin {r.choice(['', '-u ', '--force-with-lease '])}"
        assert stop_gate.targets(lead + r.choice(forms(b)), b), f"seed {SEED + 2} {b}"
        assert not stop_gate.targets(f"{lead}{b}-fix", b), f"seed {SEED + 2} {b}-fix"
        assert not stop_gate.targets(f"{lead}feat/{b}", b), f"seed {SEED + 2} feat/{b}"


@case
def property_a_merge_hidden_among_other_commands_is_denied_below_merged_and_passes_at_merged():
    r = random.Random(SEED + 3)
    cfg = dict(stop_gate.DEFAULTS)
    for k in range(300):
        parts = [r.choice(BENIGN) for _ in range(r.randint(0, 3))]
        parts.insert(r.randint(0, len(parts)), r.choice(["gh pr merge 7 --squash", "gh pr merge --auto", "gh -R o/r pr merge 7"]))
        raw = parts[0]
        for p in parts[1:]:
            raw += r.choice(SEPS) + p
        for lvl in ("commit", "pr", "ready"):
            assert stop_gate.denial(raw, lvl, cfg, ".") is not None, f"seed {SEED + 3} run {k} {lvl}: {raw!r}"
        assert stop_gate.denial(raw, "merged", cfg, ".") is None, f"seed {SEED + 3} run {k} merged: {raw!r}"


@case
def property_the_last_word_sets_the_stop_point_and_any_other_word_means_pr():
    r = random.Random(SEED + 4)
    for k in range(300):
        words = [r.choice(["fix", "the", "commit", "merged", "ready", "SHOP-42", "pr"]) for _ in range(r.randint(0, 5))]
        last = r.choice(stop_gate.LEVELS + ["SHOP-1", "Ready.", "MERGED!"])
        want = last.lower().rstrip(".!") if last.lower().rstrip(".!") in stop_gate.LEVELS else "pr"
        got = stop_gate.level_of(" ".join(words + [last]))
        assert got == want, f"seed {SEED + 4} run {k}: {words + [last]} -> {got}"


print(f"\nseed {SEED}")
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
