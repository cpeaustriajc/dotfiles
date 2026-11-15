#!/usr/bin/env python3
"""Tests replay.py: whole runs of the CLI on throwaway git repos.

Run: python3 -I test_replay.py
Fixture lines are single-line strings, so the guard's own scan of this file sees no marker.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPLAY = os.path.join(HERE, "replay.py")
passed = failed = 0
ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def report(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {detail}")


def git(root, *args):
    r = subprocess.run(["git", *args], cwd=root, env=ENV, capture_output=True, text=True)
    assert r.returncode == 0, f"git {' '.join(args)}: {r.stderr}"
    return r.stdout


def L(*lines):
    return "\n".join(lines) + "\n"


class Repo:
    """A throwaway repository; commit() takes path -> text, or None to delete."""

    def __init__(self, init=True):
        self.root = os.path.realpath(tempfile.mkdtemp(prefix="replay-"))
        if init:
            git(self.root, "init", "-q", "-b", "main")

    def commit(self, files, msg="c"):
        for path, text in files.items():
            full = os.path.join(self.root, path)
            if text is None:
                os.remove(full)
                continue
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as f:
                f.write(text)
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "--allow-empty", "-m", msg)

    def replay(self, *args, cwd=None):
        r = subprocess.run([sys.executable, "-I", REPLAY, *args], cwd=cwd or self.root, env=ENV, capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr

    def counts(self, *args, cwd=None):
        rc, out, err = self.replay(*args, cwd=cwd)
        return rc, (json.loads(out) if out.strip() else None), err

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


T = "tests/a.test.ts"
T_HEAD = L("it('sends once', () => {", "  expect(send).toHaveBeenCalledTimes(1)", "})")
P = "tests/test_b.py"
P_HEAD = L("def test_b():", "    assert b() == 1")
C = "tests/c.test.ts"
SKIPPED = "@pytest.mark" + ".skip"  # split so the guard's scan of this file finds no marker

# Root c0, then an honest value change, an added test, an added skip marker, a deleted test file, a new test file.
HISTORY = [
    {T: T_HEAD, P: P_HEAD, C: L("it('c', () => {", "  expect(c).toBe(1)", "})"), "src/a.ts": "a\n"},
    {T: T_HEAD.replace("Times(1)", "Times(2)"), "src/a.ts": "b\n"},
    {T: T_HEAD.replace("Times(1)", "Times(2)") + "it('more', () => {})\n"},
    {P: SKIPPED + "\n" + P_HEAD},
    {C: None},
    {"tests/d.test.ts": "it('d', () => {})\n"},
]


def fresh(history):
    repo = Repo()
    for files in history:
        repo.commit(files)
    return repo


def run_case(name, repo, args, want_rc, want):
    """want: a dict the counts must equal, or a substring of the error."""
    try:
        rc, counts, err = repo.counts(*args)
        ok = rc == want_rc and (counts == want if isinstance(want, dict) else want in (counts or {}).get("error", ""))
        report(name, ok, f"rc={rc} counts={counts} err={err}")
    finally:
        repo.close()


run_case("the history is counted: guarded changes, full-rule asks and rig-rule asks", fresh(HISTORY), [], 0,
         {"commits": 6, "changes": 4, "full": 3, "rigs": 1, "capped": False})

files = {f"tests/t{i}.test.ts": "a\n" for i in range(301)}
run_case("the replay stops at 300 file changes and says so", fresh([files, {p: "b\n" for p in files}]), [], 0,
         {"commits": 1, "changes": 300, "full": 300, "rigs": 0, "capped": True})

run_case("a repo with one commit has no guarded change", fresh(HISTORY[:1]), [], 0,
         {"commits": 1, "changes": 0, "full": 0, "rigs": 0, "capped": False})
run_case("a history with no test change counts none", fresh([HISTORY[0], {"src/a.ts": "b\n"}]), [], 0,
         {"commits": 2, "changes": 0, "full": 0, "rigs": 0, "capped": False})
run_case("a repo with no commit yet counts none", Repo(), [], 0, {"commits": 0, "changes": 0, "full": 0, "rigs": 0, "capped": False})
run_case("--commits reads only the latest commits", fresh(HISTORY), ["--commits", "2"], 0,
         {"commits": 2, "changes": 1, "full": 1, "rigs": 0, "capped": False})

bare = Repo(init=False)
run_case("outside a repository it exits 2 with an error", bare, [], 2, "not a git repository")

repo = fresh([{T: T_HEAD}, {T: T_HEAD + "it('b', () => {})\n"}])
git(repo.root, "checkout", "-q", "-b", "side", "HEAD~1")
repo.commit({T: T_HEAD.replace("Times(1)", "Times(3)")}, "side")
git(repo.root, "checkout", "-q", "main")
git(repo.root, "merge", "-q", "--no-edit", "--no-ff", "-X", "theirs", "side")
rc, counts, err = repo.counts()
report("a merge commit is skipped", rc == 0 and counts["commits"] == 3 and counts["changes"] == 2, f"{rc} {counts} {err}")
repo.close()

CI = L("jobs:", "  test:", "    steps:", "      - run: npm test")
run_case("a workflow that loses its test step counts as a full-rule ask", fresh([{".github/workflows/ci.yml": CI}, {".github/workflows/ci.yml": CI.replace("      - run: npm test\n", "")}]),
         [], 0, {"commits": 2, "changes": 1, "full": 1, "rigs": 0, "capped": False})
run_case("a package.json is not counted: shared files have no HEAD-line rule and are not replayed",
         fresh([{"package.json": '{"scripts": {"test": "jest"}}\n'}, {"package.json": '{"scripts": {"test": "vitest"}}\n'}]),
         [], 0, {"commits": 2, "changes": 0, "full": 0, "rigs": 0, "capped": False})

repo = fresh([{"tests/test_x.py": P_HEAD}, {"tests/test_x.py": P_HEAD + "import sys\nsys.exit(0)\n"}])
rc, counts, err = repo.counts()
report("an added early exit counts in both rule sets", rc == 0 and (counts["full"], counts["rigs"]) == (1, 1), f"{rc} {counts} {err}")
repo.close()

repo = fresh([{"checks/h.py": "a = 1\n"}, {"checks/h.py": "a = 2\n"}])
rc, plain, _ = repo.counts()
conf = os.path.join(repo.root, "cfg.json")
with open(conf, "w") as f:
    json.dump({"mode": "off", "extra_test_dirs": ["checks"]}, f)
rc2, extra, _ = repo.counts("--config", conf)
report("--config adds a project's test folders to the replay, and ignores its mode",
       (plain["changes"], extra["changes"], extra["full"]) == (0, 1, 1), f"{plain} {extra}")
repo.close()

repo = fresh(HISTORY[:2])
os.makedirs(os.path.join(repo.root, "tests"), exist_ok=True)
rc, counts, err = repo.counts(cwd=os.path.join(repo.root, "tests"))
report("it runs from a subfolder of the repository", rc == 0 and counts["changes"] == 1, f"{rc} {counts} {err}")
rc, out, err = repo.replay()
report("it prints one JSON line", out.count("\n") == 1 and err == "", f"{out!r} {err!r}")
repo.close()

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
