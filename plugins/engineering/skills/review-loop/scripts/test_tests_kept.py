#!/usr/bin/env python3
"""Tests tests_kept.py: pure cases on check(), whole runs on throwaway git repos, and properties.

Run: uv run --quiet --no-project --with hypothesis python3 -I test_tests_kept.py
Without Hypothesis, the properties run on 300 seeded random examples each, with no shrinking.
Fixture lines are single-line strings, so the check's own scan of this file sees no marker.
"""
import os
import random
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tests_kept import check, count, is_test, lost_lines  # noqa: E402

SCRIPT = os.path.join(HERE, "tests_kept.py")
passed = failed = 0


def report(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {detail}")


def L(*lines):
    return "\n".join(lines) + "\n"


PY = L("import unittest", "", "class T(unittest.TestCase):", "    def test_one(self):",
       "        self.assertEqual(add(1, 2), 3)", "", "    def test_two(self):", "        assert add(2, 2) == 4")
JS = L("import { add } from '../src/add'", "test('adds', () => {", "  expect(add(1, 2)).toBe(3)", "})")


def causes(base, now):
    return "\n".join(f"{p}:{n}: {c}" for p, n, c in check(base, now)[0])


def case(name, base, now, want):
    """want None: no findings; else a substring of the findings."""
    text = causes(base, now)
    ok = text == "" if want is None else want in text
    report(name, ok, text or "no findings")


B = {"tests/test_add.py": PY, "src/add.test.ts": JS, "src/add.py": "def add(a, b):\n    return a + b\n"}


KEY = {"py": "tests/test_add.py", "ts": "src/add.test.ts", "src": "src/add.py"}


def bend(**changes):
    now = dict(B)
    for key, text in changes.items():
        if text is None:
            now.pop(KEY[key])
        else:
            now[KEY[key]] = text
    return now


# check(): the line rule
case("an unchanged tree passes", B, dict(B), None)
case("an added test passes", B, bend(py=PY + L("    def test_three(self):", "        assert add(0, 0) == 0")), None)
case("a changed expected value is reported", B, bend(py=PY.replace("== 4", "== 5")), "tests/test_add.py:8: changes or removes base line 8")
case("a weaker matcher is reported", B, bend(ts=JS.replace("toBe(3)", "toBeDefined()")), "src/add.test.ts:3:")
case("a deleted test file is reported", B, bend(py=None), "tests/test_add.py:1: test file deleted or renamed")
case("a removed test is reported", B, bend(py=L(*PY.splitlines()[:6])), "base line 7")
case("a moved line is reported", B, bend(ts=L("test('adds', () => {", "import { add } from '../src/add'", "  expect(add(1, 2)).toBe(3)", "})")), "src/add.test.ts:2:")
case("a blank line removed passes", B, bend(py=PY.replace("\n\n", "\n")), None)
case("a code change outside tests passes", B, bend(src="def add(a, b):\n    return b + a\n"), None)
case("a dropped test count is reported", B, bend(py=PY.replace("def test_two", "def helper_two")), "tests dropped from 2 to 1")
case("a dropped assertion count is reported", B, bend(ts=JS.replace("expect(add(1, 2)).toBe(3)", "add(1, 2)")), "assertions dropped from 1 to 0")
case("a total drop is reported", B, bend(py=None), "(all test files):0: tests dropped from 3 to 1")

# check(): rigs on added lines
skip = "    @pytest.mark.skip"
case("a skip marker is reported", B, bend(py=PY.replace("    def test_two", skip + "\n    def test_two")), "adds a skip, only or xfail marker")
case("an xfail marker is reported", B, bend(py=PY + L("@pytest.mark.xfail", "def test_x():", "    assert 0")), "xfail")
case("a test.only is reported", B, bend(ts=JS + L("test.only('x', () => {})")), "skip, only")
case("a Go t.Skip is reported", {}, {"add_test.go": L("func TestAdd(t *testing.T) {", "\tt.Skip()", "}")}, "skip")
case("sys.exit(0) in a test file is reported", B, bend(py="import sys\nsys.exit(0)\n" + PY), "adds an early exit")
case("os._exit in conftest.py is reported", {}, {"conftest.py": "import os\nos._exit(0)\n"}, "early exit")
case("an exit that reports failures passes", {}, {"tests/test_x.py": "def test_a():\n    assert 1\nsys.exit(1 if failed else 0)\n"}, None)
case("exit 0 in a shell test is reported", {}, {"scripts/test_x.sh": "exit 0\necho \"ok   a\"\n"}, "adds an early exit to a shell test")
case("exit 0 after && in a shell test is reported", {}, {"scripts/test_x.sh": "[[ -n $CI ]] && exit 0\n"}, "early exit to a shell test")
case("exit 0 inside quoted text passes", {}, {"scripts/test_x.sh": 'echo "exit 0 is a pass"\n'}, None)
case("a TestReport patch is reported", {}, {"conftest.py": L("def pytest_runtest_makereport(item, call):", "    rep.outcome = 'passed'")}, "pytest report or collection hook")
case("an __eq__ override in a test file is reported", {}, {"tests/helpers.py": L("class Any:", "    def __eq__(self, other):", "        return True")}, "__eq__ override")
case("an __eq__ in source code passes", {}, {"src/money.py": L("class Money:", "    def __eq__(self, other):", "        return self.c == other.c")}, None)
case("continue-on-error in a workflow is reported", {}, {".github/workflows/ci.yml": L("    - run: pytest", "      continue-on-error: true")}, "continue-on-error")
case("|| true after a test command is reported", {}, {".github/workflows/ci.yml": L("    - run: pytest || true")}, "(|| true)")
case("|| true after a test script is reported", {}, {"package.json": L('  "scripts": { "test": "jest || true" }')}, "(|| true)")
case("|| true after a non-test command passes", {}, {"scripts/setup.sh": L("rm -f out.log || true")}, None)
case("a hook bypass in a script is reported", {}, {"scripts/ship.sh": L("git commit -m wip --no-" "verify")}, "hook bypass")
case("a hook bypass in a Markdown file passes", {}, {"README.md": L("Never pass --no-" "verify.")}, None)
case("a bunfig preload is reported", {}, {"mods/x/bunfig.toml": L("[test]", "preload = ['./rig.ts']")}, "preloads code")
case("a rig finding names the added line's number", B, bend(src=None, ts=JS + L("test.only('x', () => {})")), "src/add.test.ts:5: adds a skip")
case("a rig on an even line names that line", {}, {"tests/test_s.py": L("def test_s():", "    pytest.skip()")}, "tests/test_s.py:2: adds a skip")
case("an exit inside a string is data", {}, {"tests/test_q.py": L("MSG = 'sys.exit(0)'", "def test_q():", "    assert MSG")}, None)
case("an __eq__ inside a string is data", {}, {"tests/test_w.py": L("DOC = 'def __eq__(self, o):'", "def test_w():", "    assert DOC")}, None)
case("a per-file assertion drop names line 1", B, bend(ts=JS.replace("expect(add(1, 2)).toBe(3)", "add(1, 2)")), "src/add.test.ts:1: assertions dropped from 1 to 0")
case("a per-file drop names line 1", B, bend(py=PY.replace("def test_two", "def helper_two")), "tests/test_add.py:1: tests dropped from 2 to 1")
case("a total assertion drop names line 0", B, bend(ts=None), "(all test files):0: assertions dropped from 3 to 2")
case("a hook bypass in a Python subprocess call is reported", {}, {"scripts/ship.py": L("run(['git', 'commit', '--no-" "verify'])")}, "hook bypass")
case("a hook bypass with no test word in a script is reported", {}, {"scripts/ship.sh": L("HUSKY" "=0 git commit -m wip")}, "hook bypass")
case("TestReport inside a string is data", {}, {"tests/test_r.py": L("DOC = 'TestReport'", "def test_r():", "    assert DOC")}, None)
case("exit 0 in a Python test file is not a shell exit", {}, {"tests/test_e.py": L("def test_e():", "    assert 1", "exit 0 means pass")}, None)
case("exit 0 in a shell script that is not a test passes", {}, {"scripts/setup.sh": L("[[ -f x ]] && exit 0")}, None)
case("a marker inside a string is data", {}, {"tests/test_m.py": L("FIXTURE = '@pytest.mark.skip'", "def test_m():", "    assert FIXTURE")}, None)
case("a rig already at the base is not reported", {"tests/test_a.py": skip + "\ndef test_a():\n    assert 1\n"},
     {"tests/test_a.py": skip + "\ndef test_a():\n    assert 1\n"}, None)

# test files, the same names and folders as mods/test-guard
for path, want in [("a/b.test.ts", True), ("a/b.spec.js", True), ("test_x.py", True), ("x_test.go", True),
                   ("scripts/test_x.sh", True), ("tests/run.py", True), ("e2e/flow.ts", True),
                   ("src/__snapshots__/a.snap", True), ("src/contest.py", False), ("src/testing.py", False),
                   ("latest/x.py", False)]:
    report(f"is_test({path}) is {want}", is_test(path) == want)
for path, want in [("conftest.py", True), ("pkg/conftest.py", True), ("out/a.snap", True), ("cmd/out.golden", True),
                   ("pkg/testdata/in.json", True), ("pkg/conftest.pyc", False), ("a.snapshot.md", False)]:
    report(f"is_test({path}) is {want}", is_test(path) == want)
case("a snap file with a base line lost is reported by the lost-line rule alone", {"out/a.snap": L("a", "b")},
     {"out/a.snap": L("a")}, "changes or removes base line 2")
case("a snap file shows no count finding", {"out/a.snap": L("a", "b")}, {"out/a.snap": L("a", "b", "c")}, None)

# counting
report("counts pytest, unittest and case() tests",
       count(L("def test_a():", "async def test_b():", "case('x', f, None)", "def helper():"), "t.py")[0] == 3)
report("counts this repo's shell ok lines", count(L('echo "ok   a"', "pass=$((pass + 1))"), "t.sh") == (2, 0))
report("counts Go tests and subtests", count(L("func TestA(t *testing.T) {", '\tt.Run("x", f)', '\tt.Errorf("no")'), "a_test.go") == (2, 1))
report("lost_lines keeps test-guard's first lost line",
       lost_lines("a\nb\nc\n", "a\nc\nb\n") == [(3, "c")])


# whole runs on throwaway git repos
def run_git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull})


def repo(files):
    d = tempfile.mkdtemp(prefix="tests-kept-")
    run_git(d, "init", "-q", "-b", "main")
    write(d, files)
    run_git(d, "add", "-A")
    run_git(d, "commit", "-q", "-m", "base")
    return d


def write(d, files):
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)


def script(d, *args, env=None):
    env = {**{k: v for k, v in os.environ.items() if k != "GITHUB_BASE_REF"}, **(env or {})}
    r = subprocess.run([sys.executable, "-I", SCRIPT, *args], cwd=d, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout


def run_case(name, setup, args, want_code, want_out, env=None):
    d = repo(B)
    try:
        setup(d)
        code, out = script(d, *args, env=env)
        report(name, code == want_code and want_out in out, f"exit {code}: {out.strip()}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def commit_edit(d):
    write(d, {"tests/test_add.py": PY.replace("== 4", "== 5")})
    run_git(d, "commit", "-qam", "weaken")


def bash_rm(d):
    os.remove(os.path.join(d, "src/add.test.ts"))


def add_untracked(d):
    write(d, {"tests/test_new.py": "def test_new():\n    assert 1\n"})


def rename_main(d):
    run_git(d, "branch", "-m", "main", "trunk")


def base_ref(d):
    run_git(d, "update-ref", "refs/remotes/origin/trunk", "HEAD")
    commit_edit(d)


def origin_head(d):
    base_ref(d)
    run_git(d, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/trunk")


def no_newline(d):
    write(d, {"tests/test_tail.py": "def test_t():\n    assert x == 1"})
    run_git(d, "add", "-A")
    run_git(d, "commit", "-qm", "tail")


def one_more(d):
    write(d, {"tests/test_one.py": "def test_one():\n    assert 1\n"})
    run_git(d, "add", "-A")
    run_git(d, "commit", "-qm", "one")


def base_rig(d):
    write(d, {"scripts/ci.sh": "pytest || true\necho one\n"})
    run_git(d, "add", "-A")
    run_git(d, "commit", "-qm", "rig at base")
    write(d, {"scripts/ci.sh": "pytest || true\necho two\n"})


def origin_main(d):
    run_git(d, "update-ref", "refs/remotes/origin/main", "HEAD")
    commit_edit(d)


run_case("a clean tree passes with the counts line", lambda d: None, ["--base", "HEAD"], 0,
         "tests kept: 3 tests, 3 assertions (base: 3, 3)")
run_case("a committed weaker test fails against the base", commit_edit, ["--base", "HEAD~1"], 1,
         "tests/test_add.py:8: changes or removes base line 8: `assert add(2, 2) == 4`")
run_case("a test file removed outside the editor fails", bash_rm, ["--base", "HEAD"], 1,
         "src/add.test.ts:1: test file deleted or renamed")
run_case("an untracked new test counts", add_untracked, ["--base", "HEAD"], 0, "tests kept: 4 tests, 4 assertions")
run_case("the default base is the merge-base with origin/main", origin_main, [], 1, "tests/test_add.py:8:")
run_case("the default base is origin/$GITHUB_BASE_REF in CI", base_ref, [], 1, "tests/test_add.py:8:", env={"GITHUB_BASE_REF": "trunk"})
run_case("without GITHUB_BASE_REF origin/trunk is not a base", base_ref, [], 2, "no base")
run_case("the default base is origin/HEAD when set", origin_head, [], 1, "tests/test_add.py:8:")
run_case("a base file with no final newline reads whole", no_newline, ["--base", "HEAD"], 0, "tests kept: 4 tests, 4 assertions (base: 4, 4)")
run_case("the base counts add every file", one_more, ["--base", "HEAD"], 0, "(base: 4, 4)")
run_case("a rig already in a changed file is not new", base_rig, ["--base", "HEAD"], 0, "tests kept:")
run_case("no remote and no --base exits 2", rename_main, [], 2, "tests kept: could not check: no base")
run_case("a base that is not a commit exits 2", lambda d: None, ["--base", "nope"], 2, "nope is not a commit")
nogit = tempfile.mkdtemp(prefix="tests-kept-nogit-")
code, out = script(nogit)
report("outside a git repo exits 2", code == 2 and "not a git repository" in out, f"exit {code}: {out}")
shutil.rmtree(nogit, ignore_errors=True)


# properties
LINES = ["def test_a():", "    assert f(1) == 2", "    self.assertEqual(x, 1)", "test('x', () => {", "  expect(y).toBe(1)",
         "})", "x = 1", "", "    return", "# note", 'echo "ok   a"']


def prop_adding_never_lowers(base_lines, extra, at):
    base = "\n".join(base_lines) + "\n"
    lines = list(base_lines)
    lines[at % (len(lines) + 1):at % (len(lines) + 1)] = extra
    now = "\n".join(lines) + "\n"
    for path in ("tests/t.py", "t.test.ts"):
        f, (n0, m0), (n1, m1) = check({path: base}, {path: now})
        assert n1 >= n0 and m1 >= m0, (base_lines, extra, at)
        assert not [c for _p, _n, c in f if "base line" in c or "dropped" in c], f


def prop_removing_is_reported(base_lines, at):
    if not any(line.strip() for line in base_lines):
        return
    keep = [i for i, line in enumerate(base_lines) if line.strip()]
    drop = keep[at % len(keep)]
    now = "\n".join(line for i, line in enumerate(base_lines) if i != drop) + "\n"
    f = check({"tests/t.py": "\n".join(base_lines) + "\n"}, {"tests/t.py": now})[0]
    assert any("base line" in c for _p, _n, c in f), (base_lines, drop)


def run_props():
    try:
        from hypothesis import given, settings, strategies as st
    except ImportError:
        rnd = random.Random(20261113)
        pick = lambda k: [rnd.choice(LINES) for _ in range(rnd.randint(k, 12))]  # noqa: E731
        for name, prop, gen in [("adding lines never lowers a count", prop_adding_never_lowers,
                                 lambda: (pick(0), pick(1), rnd.randint(0, 20))),
                                ("removing any base test line is reported", prop_removing_is_reported,
                                 lambda: (pick(1), rnd.randint(0, 20)))]:
            try:
                for _ in range(300):
                    prop(*gen())
                report(f"{name} (300 seeded examples, no Hypothesis)", True)
            except AssertionError as e:
                report(name, False, e)
        return
    text = st.lists(st.one_of(st.sampled_from(LINES), st.text(alphabet="ab()=' \t#", max_size=12)), max_size=12)
    for name, prop, args in [("adding lines never lowers a count", prop_adding_never_lowers,
                              (text, text.filter(bool), st.integers(0, 20))),
                             ("removing any base test line is reported", prop_removing_is_reported,
                              (text.filter(bool), st.integers(0, 20)))]:
        try:
            settings(max_examples=300, deadline=None)(given(*args)(prop))()
            report(f"{name} (Hypothesis, 300 examples)", True)
        except AssertionError as e:
            report(name, False, e)


run_props()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
