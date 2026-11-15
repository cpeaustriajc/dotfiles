#!/usr/bin/env python3
"""Holds an /implement run to the stop point the user typed: a command hook for Claude Code.

One script, three events, read from the hook JSON on stdin (`hook_event_name`):

- UserPromptSubmit: `/implement ... <word>` (or `/<plugin>:implement ...`) saves the stop point;
  `/implement-gate` shows it and `/implement-gate off` ends the gate.
- PreToolUse (Bash, MCP tools, Edit/Write/MultiEdit): denies a merge, a push, a write to branch
  protection, or an edit of the gate's own files, past the stop point.
- Stop: blocks the turn's end while the pull request is short of the stop point.

Project facts come from `stop_gate.json` beside this file (every key is optional):
  default_branch  a name, or null to read origin/HEAD and else use main and master
  merge_tools     MCP tool-name substrings that merge (case-insensitive)
  push_tools      MCP tool-name substrings that push (case-insensitive)
  max_blocks      Stop blocks per head commit before the Stop passes (default 3)

State lives outside the working tree: $TMPDIR/claude-hooks/<session_id>/stop-gate.json.
PreToolUse fails closed, Stop fails open, UserPromptSubmit fails open.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
MOD = "implement-gate"
LEVELS = ["commit", "pr", "ready", "merged"]
# A hung gh or git (network, an auth prompt) must not hold the turn's end.
TIMEOUT_S = 20
GREEN = {"SUCCESS", "NEUTRAL", "SKIPPED"}
FIELDS = "url,state,headRefOid,isDraft,autoMergeRequest,mergeable,reviewDecision,statusCheckRollup"
OFF = "The user can type /implement-gate off to end the gate."
TEXT = "If those words are only text, such as a commit message, write the text to a file and pass the file."
EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}

DEFAULTS = {
    "default_branch": None,
    "merge_tools": ["merge_pull_request", "merge_merge_request", "automerge", "auto_merge"],
    "push_tools": ["push_files", "create_or_update_file"],
    "max_blocks": 3,
}


def rank(level):
    return LEVELS.index(level)


# --- config ------------------------------------------------------------------------------------

def load_config(path=None):
    """The config beside this file, key by key; a missing file, a missing key or a wrong type
    gives today's default."""
    cfg = dict(DEFAULTS)
    try:
        with open(path or os.path.join(HERE, "stop_gate.json"), encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError):
        return cfg
    if not isinstance(raw, dict):
        return cfg
    if isinstance(raw.get("default_branch"), str) and raw["default_branch"].strip():
        cfg["default_branch"] = raw["default_branch"].strip()
    for key in ("merge_tools", "push_tools"):
        v = raw.get(key)
        if isinstance(v, list) and all(isinstance(s, str) for s in v):
            cfg[key] = v
    m = raw.get("max_blocks")
    if isinstance(m, int) and not isinstance(m, bool) and m >= 0:
        cfg["max_blocks"] = m
    return cfg


# --- state -------------------------------------------------------------------------------------

def state_path(session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "") or "_"
    safe = re.sub(r"^\.", "_", safe)
    base = os.environ.get("TMPDIR") or "/tmp"
    return os.path.join(base, "claude-hooks", safe, "stop-gate.json")


def read_state(session_id):
    """No file: no run is gated. A file that does not parse raises, so PreToolUse fails closed."""
    try:
        with open(state_path(session_id), encoding="utf-8") as f:
            st = json.load(f)
    except FileNotFoundError:
        return {"level": None, "blocks": 0, "head": None}
    level = st.get("level")
    if level is not None and level not in LEVELS:
        raise ValueError(f"unknown stop point {level!r} in {state_path(session_id)}")
    return {"level": level, "blocks": int(st.get("blocks") or 0), "head": st.get("head")}


def write_state(session_id, st):
    path = state_path(session_id)
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".stop-gate-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(st, f)
    os.replace(tmp, path)


def begin(session_id, level):
    write_state(session_id, {"level": level, "blocks": 0, "head": None})


# --- command text ------------------------------------------------------------------------------

def level_of(args):
    """Only the last word: "/implement fix the commit hook SHOP-42" must not read as `commit`."""
    words = args.strip().lower().split()
    last = re.sub(r"[^a-z]+$", "", words[-1]) if words else ""
    return last if last in LEVELS else "pr"


# The command split at `&&`, `||`, `;`, `|` and line ends, with `\` line breaks joined. Quotes are
# not parsed: a parser of shell text misses forms, and a missed merge passes in silence. Text that
# names a merge is denied instead, which is visible, and the deny says how to get around it.
def segments(raw):
    return re.split(r"&&|\|\||;|\||\r?\n", re.sub(r"\\\r?\n", " ", raw))


A = re.A
GH = re.compile(r"\bgh\b", A)
# `merge` as a word, not `merge-base`; and the GraphQL merge mutations.
MERGE = re.compile(r"\bmerge\b(?!-)|mergePullRequest|enablePullRequestAutoMerge", A | re.I)
GRAPHQL_MERGE = re.compile(r"\bgh\s+api\s+graphql\b[\s\S]*\b(mergePullRequest|enablePullRequestAutoMerge)\b", A)
PUSH = re.compile(r"\bgit\b.*\bpush\b(.*)", A)
CREATE = re.compile(r"\bpr\s+create\b", A)
# A write to branch protection or a ruleset: the gate rests on them (an agent was seen to null the
# required checks, merge, and put them back). A read (no method, no field) passes.
PROTECTION = re.compile(r"\bgh\s+api\b.*\b(branches/\S+/protection|rulesets)\b", A)
WRITE = re.compile(
    r"(-X|--method)[\s=]*['\"]?(PUT|PATCH|POST|DELETE)\b|\s(-f|-F|--field|--raw-field|--input)[\s=]", A | re.I)


def targets(rest, branch):
    """A default branch named as a push target: `main`, `HEAD:main`, `+refs/heads/main`, `"main"`."""
    return any(re.sub(r"^refs/heads/", "", w) == branch for w in re.split(r"[\s:+'\"=()]+", rest))


# --- git and gh --------------------------------------------------------------------------------

def run(argv, cwd):
    """stdout, or an Error: a failed spawn, a timeout and a non-zero exit all keep their message."""
    try:
        r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return Error(f"{argv[0]} took over {TIMEOUT_S} seconds")
    except (OSError, ValueError) as e:
        return Error(str(e))
    if r.returncode == 0:
        return r.stdout
    return Error(r.stderr.strip() or f"{argv[0]} exited {r.returncode}")


class Error(Exception):
    pass


def default_branches(cfg, cwd):
    if cfg["default_branch"]:
        return [cfg["default_branch"]]
    r = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], cwd)
    if isinstance(r, Error):
        return ["main", "master"]
    return [re.sub(r"^origin/", "", r.strip())]


def denial(raw, level, cfg, cwd):
    below = rank(level) < rank("merged")
    pushes = []
    for s in segments(raw):
        merging = GH.search(s) and MERGE.search(s)
        if merging and re.search(r"--admin\b", s):
            return "bypasses branch protection with --admin"
        if PROTECTION.search(s) and WRITE.search(s):
            return "changes branch protection or a ruleset"
        if merging and below and not re.search(r"--disable-auto\b", s):
            return f"merges the PR or turns on auto-merge. {TEXT}"
        push = PUSH.search(s)
        if level == "commit" and (push or (GH.search(s) and CREATE.search(s))):
            return "pushes or opens a PR"
        if push:
            pushes.append(push.group(1))
    if below and GRAPHQL_MERGE.search(raw):
        return f"merges the PR or turns on auto-merge. {TEXT}"
    if below and pushes:
        for b in default_branches(cfg, cwd):
            if any(targets(p, b) for p in pushes):
                return f"pushes to the default branch {b}"
    return None


# --- the pull request --------------------------------------------------------------------------

def running(c):
    return (c.get("status") or "COMPLETED") != "COMPLETED" or c.get("state") in ("PENDING", "EXPECTED")


def failing(pr):
    for c in pr.get("statusCheckRollup") or []:
        if not running(c) and (c.get("conclusion") or c.get("state") or "SUCCESS") not in GREEN:
            return f"a check failed on {pr['url']}. Fix it and push"
    if pr.get("reviewDecision") == "CHANGES_REQUESTED":
        return f"a review requests changes on {pr['url']}"
    if pr.get("mergeable") == "CONFLICTING":
        return f"{pr['url']} conflicts with its base. Rebase it"
    return None


def gap(level, pr):
    if pr is None:
        return "no PR is open for this branch. Open it with create-pr"
    if pr["state"] == "MERGED":
        return None
    if pr["state"] != "OPEN":
        return f"{pr['url']} is {pr['state'].lower()}. Ask the user with AskUserQuestion"
    if level == "pr":
        return None
    if level == "ready" and pr.get("autoMergeRequest"):
        return f"auto-merge is on for {pr['url']}. Turn it off with gh pr merge --disable-auto"
    if pr.get("isDraft"):
        return f"{pr['url']} is a draft. Mark it ready with gh pr ready"
    bad = failing(pr)
    if bad:
        return bad
    # Auto-merge waits for running checks itself; `ready` must see them finish.
    if level == "merged" and pr.get("autoMergeRequest"):
        return None
    if any(running(c) for c in pr.get("statusCheckRollup") or []):
        return (f"checks are still running on {pr['url']}. Wait in the foreground with gh pr checks --watch "
                "(Bash timeout 600000); a waiting command spends no tokens")
    if level == "ready":
        return None
    return f"the gate holds on {pr['url']}, but auto-merge is off. Turn it on with gh pr merge --auto"


def view_pr(cwd):
    """The PR dict, None when the branch has none, or an Error."""
    r = run(["gh", "pr", "view", "--json", FIELDS], cwd)
    if isinstance(r, Error):
        return None if re.search(r"no pull requests found", str(r), re.I) else r
    try:
        pr = json.loads(r)
        if not isinstance(pr, dict) or not isinstance(pr.get("state"), str):
            raise ValueError("gh pr view returned no state")
    except ValueError as e:
        return Error(str(e))
    if pr["state"] != "MERGED":
        return pr
    # A merged PR from an earlier use of this branch name is not this run's PR.
    local = run(["git", "rev-parse", "HEAD"], cwd)
    if isinstance(local, Error):
        return local
    return pr if local.strip() == pr.get("headRefOid") else None


# --- events ------------------------------------------------------------------------------------

def emit(obj):
    sys.stdout.write(json.dumps(obj))
    sys.stdout.flush()


def deny(reason):
    emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                 "permissionDecisionReason": reason}})


IMPLEMENT = re.compile(r"\A\s*/(?:[^\s/:]+:)?implement(?:\s+(.*))?\Z", re.S)
GATE = re.compile(r"\A\s*/implement-gate(?:\s+(.*))?\Z", re.S)


def user_prompt_submit(inp):
    # UserPromptSubmit fires only for a prompt the user submitted: a model, a peer session or a
    # subagent cannot reach it. That replaces the old check of the command's origin.
    prompt = inp.get("prompt") or ""
    sid = inp.get("session_id")
    m = GATE.match(prompt)
    if m:
        if (m.group(1) or "").strip() == "off":
            begin(sid, None)
            text = "The gate is off until the next /implement."
        else:
            level = read_state(sid)["level"]
            text = (f"Stop point: {level}. Type /implement-gate off to end the gate." if level
                    else "No /implement run is gated.")
        # A block keeps the prompt from the model; the reason goes to the user.
        emit({"decision": "block", "reason": text})
        return
    m = IMPLEMENT.match(prompt)
    if m:
        level = level_of(m.group(1) or "")
        begin(sid, level)
        emit({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                     "additionalContext": f"{MOD}: stop point {level}"}})


def own_file(path, cwd):
    p = os.path.realpath(os.path.join(cwd or "", path))
    return p == HERE or p.startswith(HERE + os.sep) or p.endswith(os.sep + os.path.join(".claude", "settings.json"))


def pre_tool_use(inp, cfg):
    level = read_state(inp.get("session_id"))["level"]
    if not level:
        return
    tool = inp.get("tool_name") or ""
    tin = inp.get("tool_input") or {}
    cwd = inp.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if tool == "Bash":
        raw = str(tin.get("command") or "")
        if not re.search(r"\b(gh|git)\b", raw, A):
            return
        why = denial(raw, level, cfg, cwd)
        if why:
            what, hint = (why.replace(TEXT, "").strip(), f" {TEXT}") if TEXT in why else (why, "")
            deny(f"{MOD}: this command {what.rstrip('.')}, past the stop point `{level}` that the user typed for /implement.{hint} {OFF}")
    elif tool.startswith("mcp__"):
        low = tool.lower()
        if rank(level) < rank("merged") and any(s.lower() in low for s in cfg["merge_tools"]):
            deny(f"{MOD}: {tool} merges past the stop point `{level}`. {OFF}")
        elif level == "commit" and any(s.lower() in low for s in cfg["push_tools"]):
            deny(f"{MOD}: {tool} pushes past the stop point `commit`. {OFF}")
    elif tool in EDIT_TOOLS:
        path = tin.get("file_path")
        if isinstance(path, str) and own_file(path, cwd):
            deny(f"{MOD}: {tool} would change the gate's own files ({path}) during an /implement run. {OFF}")


def stop(inp, cfg):
    sid = inp.get("session_id")
    st = read_state(sid)
    level = st["level"]
    if not level:
        return
    cwd = inp.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

    def done():
        begin(sid, None)

    def failed(why):
        # A git or gh error lets this stop through and keeps the gate for the next one.
        emit({"systemMessage": f"{MOD}: {why}; this stop is not checked. {OFF}"})

    if level == "commit":
        return done()
    b = run(["git", "branch", "--show-current"], cwd)
    if isinstance(b, Error):
        return failed(f"could not read the branch ({b})")
    # On the default branch or a detached HEAD there is no PR to check: a coordinator run, or a
    # repo that opens none.
    if not b.strip() or b.strip() in default_branches(cfg, cwd):
        return done()
    pr = view_pr(cwd)
    if isinstance(pr, Error):
        return failed(f"could not read the PR ({pr})")
    why = gap(level, pr)
    if not why:
        return done()
    sha = pr.get("headRefOid") if pr else None
    if sha != st["head"]:
        st["head"], st["blocks"] = sha, 0
    n, limit = st["blocks"], cfg["max_blocks"]
    if n >= limit:
        # Keep the gate's denies; only stop blocking, and say so once.
        if n == limit:
            emit({"systemMessage": f"{MOD}: stopped before `{level}` after {limit} blocks: {why}. {OFF}"})
        st["blocks"] = limit + 1
        write_state(sid, st)
        return
    st["blocks"] = n + 1
    write_state(sid, st)
    emit({"decision": "block",
          "reason": f"{MOD}: /implement was typed with `{level}`, and {why}. "
                    f"If you cannot continue alone, ask with AskUserQuestion. ({n + 1} of {limit})"})


def main():
    try:
        inp = json.load(sys.stdin)
        event = inp.get("hook_event_name")
        cfg = load_config()
    except Exception:
        return 0
    try:
        if event == "UserPromptSubmit":
            user_prompt_submit(inp)
        elif event == "PreToolUse":
            pre_tool_use(inp, cfg)
        elif event == "Stop":
            stop(inp, cfg)
    except Exception as e:
        if event == "PreToolUse":
            tool = inp.get("tool_name") or "this call"
            what = "this command" if tool == "Bash" else tool
            deny(f"{MOD}: could not check {what} ({e}). Retry it. {OFF}")
        elif event == "Stop":
            emit({"systemMessage": f"{MOD}: could not check this stop ({e}); it is not checked. {OFF}"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
