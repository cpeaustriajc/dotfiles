#!/usr/bin/env python3
"""Tests guard_tests.py: the rules as pure cases, and the hook as a subprocess on throwaway git repos.

Run: python3 -I test_guard_tests.py
The hook cases pipe the JSON Claude Code sends into a copy of the scripts in <repo>/.claude/hooks, as
a project holds them after Setup. Fixture lines are single-line strings, so the guard's own scan of
this file sees no marker.
"""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import guard_tests as gt  # noqa: E402
import tests_kept as tk  # noqa: E402

passed = failed = 0
SEED = int(os.environ.get("SEED", time.time())) % 2 ** 31
RUNS = 300
ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def t(fn):
    """Runs a case now; an assert or an error in it is a failure."""
    global passed, failed
    name = fn.__name__.replace("_", " ")
    try:
        fn()
        passed += 1
        print(f"ok   {name}")
    except Exception as e:  # noqa: BLE001
        failed += 1
        print(f"FAIL {name}: {type(e).__name__}: {e}")
    return fn


def L(*lines):
    return "\n".join(lines) + "\n"


# ---- the rules, as pure cases ----

K = gt.DEFAULT.kind_of
PY = L("import pytest", "", "def test_sends():", "    assert send() == 1", "", "def test_mute():", "    assert mute() is None")
TS = L("import { send } from '../src/send'", "", "it('sends once', () => {", "  expect(send()).toBe(1)", "})")


def finding(kind, path, head, nxt, **kw):
    f = gt.findings(kind, path, head, nxt, **kw)
    return f.what if f else "no finding"


def denies(kind, path, head, nxt, what):
    got = finding(kind, path, head, nxt)
    assert what in got, f"{path}: wanted {what!r}, got {got!r}"


def passes(kind, path, head, nxt):
    f = gt.findings(kind, path, head, nxt)
    assert f is None, f"{path}: {f}"


@t
def property_an_edit_that_only_inserts_lines_never_loses_a_head_line():
    r = random.Random(SEED)
    words = ["expect(a).toBe(1)", "notify()", "})", "it('x', () => {", "x = 1", "assert y == 2", "return z", "  ", "", "a", "b"]
    for k in range(RUNS):
        head = [r.choice(words) for _ in range(r.randrange(12))]
        nxt = list(head)
        for _ in range(r.randrange(5)):
            nxt.insert(r.randrange(len(nxt) + 1), r.choice(words))
        for path in ("", "a.test.ts"):
            assert not tk.lost_lines("\n".join(head), "\n".join(nxt), path), f"seed {SEED} run {k} {path!r}"


@t
def property_removing_or_changing_any_non_blank_head_line_is_always_reported():
    r = random.Random(SEED + 1)
    words = ["expect(a).toBe(1)", "notify()", "})", "it('x', () => {", "x = 1", "assert y == 2", "return z", "  ", "", "a", "b"]
    for k in range(RUNS):
        head = [r.choice(words) for _ in range(1 + r.randrange(12))]
        full = [i for i, line in enumerate(head) if line.strip()]
        if not full:
            continue
        at = r.choice(full)
        removed = [line for i, line in enumerate(head) if i != at]
        changed = [line + " // weaker" if i == at else line for i, line in enumerate(head)]
        assert tk.lost_lines("\n".join(head), "\n".join(removed)), f"seed {SEED + 1} run {k}: removed {head[at]!r}"
        assert tk.lost_lines("\n".join(head), "\n".join(changed)), f"seed {SEED + 1} run {k}: changed {head[at]!r}"


@t
def property_an_unchanged_file_never_gets_a_finding_whatever_it_holds():
    r = random.Random(SEED + 2)
    marked = ["expect(a).toBe(1)", "notify()", "})", "x = 1", "  ", "", "@pytest.mark" + ".skip", "sys.exit(0)", "it.only(",
              "def __eq__(self, o): return True", "continue-on-error: true", "/*", "*/", '"' * 3]
    for k in range(RUNS):
        text = "\n".join(r.choice(marked) for _ in range(r.randrange(15)))
        for kind, path in (("test", "a.test.ts"), ("test", "test_a.py"), ("config", "jest.config.js"), ("shared", "package.json")):
            assert gt.findings(kind, path, text, text) is None, f"seed {SEED + 2} run {k} {path}"


@t
def property_lines_with_no_quote_or_comment_mark_are_never_hidden():
    r = random.Random(SEED + 3)
    for k in range(RUNS):
        ls = [r.choice(["a = 1", "f(x)", "})", "{", "return 2", ""]) for _ in range(r.randrange(10))]
        for kind in ("c", "py"):
            assert not any(tk.hidden(ls, kind)), f"seed {SEED + 3} run {k}"


@t
def property_apply_leaves_the_text_alone_when_old_string_is_absent_or_equals_new_string():
    r = random.Random(SEED + 4)
    words = ["expect(a).toBe(1)", "notify()", "x = 1", "a", "b", ""]
    for k in range(RUNS):
        text = "\n".join(r.choice(words) for _ in range(r.randrange(8)))
        assert gt.apply(text, {"old_string": f"absent-{k}", "new_string": "y"}) == text
        some = r.choice(words)
        assert gt.apply(text, {"old_string": some, "new_string": some, "replace_all": r.random() < 0.5}) == text


@t
def property_a_path_is_a_test_when_a_folder_from_the_repo_root_is_a_test_folder():
    r = random.Random(SEED + 5)
    dirs = ["src", "lib", "pkg", "app", "contest", "latest", "docs"]
    for k in range(RUNS):
        segs = [r.choice(dirs) for _ in range(r.randrange(4))]
        plain = "/".join(segs + [f"mod{k}.ts"])
        assert K(plain) is None, f"seed {SEED + 5} {plain}"
        folder = r.choice(["tests", "test", "__tests__", "e2e", "__snapshots__", "testdata"])
        deep = "/".join(segs[:1] + [folder] + segs[1:] + [f"mod{k}.ts"])
        assert K(deep) == "test", f"seed {SEED + 5} {deep}"


@t
def kinds_test_names_golden_files_runner_config_ci_and_shared_files():
    for p in ["conftest.py", "pkg/conftest.py", "src/__snapshots__/a.ts.snap", "cmd/out.golden", "pkg/testdata/in.json", "a.test.ts"]:
        assert K(p) == "test", p
    for p in ["jest.config.ts", "web/vitest.config.mts", "vitest.workspace.ts", "playwright.config.ts", "pytest.ini",
              ".pre-commit-config.yaml", ".github/workflows/ci.yml", ".husky/pre-commit"]:
        assert K(p) == "config", p
    for p in ["package.json", "pyproject.toml", "setup.cfg", "tox.ini"]:
        assert K(p) == "shared", p
    for p in ["src/app.ts", "docs/.github/workflows/x.md", "fixtures/a.json", "src/config.ts", "jest.setup.ts"]:
        assert K(p) is None, p
    assert not gt.DEFAULT.maybe_guarded("/repo/src/app.ts")
    assert gt.DEFAULT.maybe_guarded("/repo/.github/workflows/ci.yml")


@t
def kinds_names_that_only_start_like_a_test_name_are_not_tests():
    for p in ["pkg/test_util.pyc", "a.snapshot.md", "out.golden.bak", "notes/conftest.py.bak", "pkg/util_test.pyc", "src/a.test.d/x.ts"]:
        assert K(p) is None, p


@t
def kinds_test_star_sh_is_a_test_name_like_test_star_py():
    for p in ["test_build.sh", "scripts/test_check_video.sh"]:
        assert K(p) == "test", p
    assert K("scripts/test_build.shx") is None


@t
def a_skip_decorator_on_a_head_test_is_asked_about_on_a_new_test_it_passes():
    denies("test", "test_a.py", PY, PY.replace("def test_sends", "@pytest.mark.skip\ndef test_sends"), "skips the HEAD test `def test_sends():`")
    denies("test", "test_a.py", PY, PY.replace("def test_mute", '@pytest.mark.xfail(reason="x")\ndef test_mute'), "skips the HEAD test")
    passes("test", "test_a.py", PY, PY + '\n@pytest.mark.skipif(sys.platform == "win32", reason="posix")\ndef test_new():\n    assert 1\n')


@t
def a_skip_call_or_a_bare_return_inside_a_head_test_is_asked_about_inside_a_new_test_it_passes():
    denies("test", "test_a.py", PY, PY.replace("    assert send() == 1", '    pytest.skip("flaky")\n    assert send() == 1'), "skips the HEAD test")
    denies("test", "a.test.ts", TS, TS.replace("  expect(send()).toBe(1)", "  return\n  expect(send()).toBe(1)"),
           "skips the HEAD test `it('sends once', () => {`")
    denies("test", "x_test.go", "func TestA(t *testing.T) {\n\tcheck(t)\n}\n", "func TestA(t *testing.T) {\n\tt.Skip()\n\tcheck(t)\n}\n", "skips the HEAD test")
    passes("test", "test_a.py", PY, PY + '\ndef test_net():\n    if offline():\n        pytest.skip("no network")\n    assert get()\n')
    passes("test", "a.test.ts", TS, TS + "\nfunction helper(x) {\n  if (!x) return\n  return x\n}\n")


@t
def only_a_skipped_block_ts_nocheck_and_if_false_in_a_head_test_file_are_asked_about():
    for add in ["it.only('new', () => {})", "describe.skip('all', () => {", "// @ts-nocheck", "if (false) {", "fit('x', () => {})"]:
        denies("test", "a.test.ts", TS, f"{add}\n{TS}", "skips or focuses tests")
    denies("test", "test_a.py", PY, f"pytestmark = pytest.mark.skip\n{PY}", "skips or focuses tests")
    passes("test", "a.test.ts", TS, TS + "\nit.skip('pending: retries', () => {})\n")
    passes("test", "new.test.ts", None, "it.only('focus', () => {})\n")


@t
def a_block_comment_or_a_string_around_head_lines_is_asked_about_a_glob_string_is_not_a_comment():
    denies("test", "a.test.ts", TS, TS.replace("it('sends once'", "/*\nit('sends once'").replace("})\n", "})\n*/\n"), "comments out a line")
    denies("test", "test_a.py", PY, PY.replace("def test_mute", '"""\ndef test_mute') + '"""\n', "comments out a line")
    passes("test", "a.test.ts", TS, f"const files = glob('src/**/*.ts')\n{TS}")
    passes("test", "a.test.ts", TS, f"/** helpers */\n{TS}\n/*\n * a new note\n */\n")
    passes("test", "test_a.py", PY, PY + '\ndef test_doc():\n    """Checks the docs."""\n    assert doc()\n')


@t
def an_exit_with_success_is_asked_about_in_any_test_file_os_exit_m_run_passes():
    denies("test", "conftest.py", None, "import sys\nsys.exit(0)\n", "exits the test process")
    denies("test", "test_a.py", PY, PY + "\nos._exit(0)\n", "exits the test process")
    denies("test", "a.test.ts", TS, TS + "\nprocess.exit()\n", "exits the test process")
    passes("test", "main_test.go", None, "func TestMain(m *testing.M) {\n\tos.Exit(m.Run())\n}\n")
    passes("test", "a.test.ts", TS, TS + "\nconst exit = jest.spyOn(process, 'exit')\n")


HACK = L("from _pytest.reports import TestReport", "orig = TestReport.from_item_and_call", "def patched(*a, **k):", "    rep = orig(*a, **k)",
         '    if rep.when == "call":', '        rep.outcome = "passed"', "        rep.longrepr = None", "    return rep",
         "TestReport.from_item_and_call = patched")
HONEST = L("import pytest", "", "@pytest.fixture", "def db(tmp_path):", '    return connect(tmp_path / "db")', "",
           "@pytest.hookimpl(hookwrapper=True)", "def pytest_runtest_makereport(item, call):", "    out = yield", "    rep = out.get_result()",
           '    if rep.outcome == "failed":', "        item.stash[KEY] = rep")


@t
def a_conftest_that_rewrites_the_report_is_asked_about_an_honest_one_with_fixtures_passes():
    denies("test", "conftest.py", None, HACK, "rewrites the test report")
    denies("test", "conftest.py", None, '@pytest.hookimpl(hookwrapper=True)\ndef pytest_runtest_makereport(item, call):\n    out = yield\n'
           '    out.get_result().outcome = "passed"\n', "rewrites the test report")
    passes("test", "conftest.py", None, HONEST)


@t
def an_always_true_equality_is_asked_about_in_a_test_file_a_real_eq_passes():
    denies("test", "tests/helpers.py", None, "class Any:\n    def __eq__(self, other): return True\n", "always true")
    denies("test", "tests/helpers.py", None, "class Any:\n    def __eq__(self, other):\n        return True\n", "always true")
    denies("test", "tests/helpers.py", None, "Any.__eq__ = lambda self, o: True\n", "always true")
    denies("test", "a.test.ts", TS, TS + "\nconst any = { asymmetricMatch: () => true }\n", "always true")
    passes("test", "tests/helpers.py", None, "class Point:\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n")


CI = L("jobs:", "  test:", "    steps:", "      - run: npm test")


@t
def runner_config_a_changed_head_line_or_an_added_pass_anyway_flag_is_asked_about_an_added_job_passes():
    denies("config", ".github/workflows/ci.yml", CI, CI.replace("      - run: npm test\n", ""), "changes or removes a line")
    denies("config", ".github/workflows/ci.yml", CI, CI.replace("    steps:", "    continue-on-error: true\n    steps:"), "stops tests from running")
    denies("config", ".husky/pre-commit", "npm test\n", "npm test\nnpm test || true\n", "stops tests from running")
    passes("config", ".github/workflows/ci.yml", CI, CI + "  lint:\n    steps:\n      - run: npm run lint\n")
    passes("config", "jest.config.js", None, "module.exports = { testPathIgnorePatterns: ['/node_modules/'] }\n")


PKG = '{\n  "scripts": {\n    "test": "jest"\n  }\n}\n'


@t
def shared_files_only_an_added_pass_anyway_flag_is_asked_about():
    denies("shared", "package.json", PKG, PKG.replace('"jest"', '"jest",\n    "test:ci": "jest --passWithNoTests"'), "stops tests from running")
    denies("shared", "pyproject.toml", '[tool.pytest.ini_options]\naddopts = "-q"\n',
           '[tool.pytest.ini_options]\naddopts = "-q"\naddopts = "--deselect tests/test_a.py::test_x"\n', "stops tests")
    passes("shared", "package.json", PKG, PKG.replace('"jest"', '"vitest"'))
    passes("shared", "package.json", PKG, PKG.replace('"jest"', '"jest",\n    "clean": "rm -rf dist || true"'))


@t
def align_marks_only_the_lines_no_head_line_took_as_added():
    a = tk.align("a\nb\n", "a\nx\nb\n")
    assert a.gone == [] and a.added == [False, True, False], a


@t
def raise_system_exit_and_the_builtin_exit_with_success_are_asked_about_in_a_python_test_file_honest_exits_pass():
    for x in ["raise SystemExit", "raise SystemExit()", "raise SystemExit(0)", "raise SystemExit(None)", "exit()", "exit(0)", "quit()", "quit(0)"]:
        denies("test", "test_a.py", PY, f"{PY}\n{x}\n", "exits the test process")
    denies("test", "conftest.py", None, 'print("1 passed, 0 failed")\nraise SystemExit\n', "exits the test process")
    for x in ["sys.exit(1 if failed else 0)", "raise SystemExit(1 if failed else 0)", "raise SystemExit(main())", "sys.exit(main())",
              "raise SystemExit(1)", "exit(1)", "MSG = 'raise SystemExit'"]:
        passes("test", "test_a.py", PY, f"{PY}\n{x}\n")
    passes("test", "tests/fixtures/fake_cli.py", None, "raise SystemExit\n")


@t
def an_outcome_field_of_the_code_under_test_and_an_exit_in_a_helper_script_pass():
    passes("test", "tests/test_game.py", None, 'def test_win():\n    game.outcome = "won"\n    assert game.score == 3\n')
    passes("test", "tests/fixtures/fake_cli.py", None, 'import sys\nprint("ok")\nsys.exit(0)\n')
    denies("test", "tests/test_cli.py", None, "import sys\nsys.exit(0)\n", "exits the test process")


@t
def the_comment_scanner_quotes_escapes_line_comments_and_closed_comments_open_nothing():
    def C(src):
        return tk.hidden(src.split("\n"), "c")

    def P(src):
        return tk.hidden(src.split("\n"), "py")
    assert C("const g = 'src/*.ts'\nx") == [False, False]
    assert C('const g = "src/*.ts"\nx') == [False, False]
    assert C("const s = 'it\\'s /* not a comment'\nx") == [False, False]
    assert C("// see /* the note\nx") == [False, False]
    assert C("/* one line */ x\ny") == [False, False]
    assert C("/* open\ninside */ x\ny") == [False, True, False]
    assert C("const t = `a\\` /* b\nc`\nd") == [False, True, False]
    assert C("const t = `a\nb`\nc") == [False, True, False]
    assert P('# a """ in a comment\nx') == [False, False]
    assert P("s = '\"\"\"'\nx") == [False, False]
    assert P('"""doc\nmore\n"""\nx') == [False, True, True, False]
    assert P('s = "a\\"b"\nx = 1  # """\ny') == [False, False, False]


@t
def a_removed_head_line_is_named_as_removed_not_as_commented_out():
    assert "changes or removes" in finding("test", "a.test.ts", TS, TS.replace("  expect(send()).toBe(1)\n", ""))


@t
def a_bare_return_added_to_a_head_helper_not_a_test_passes():
    head = f"{TS}\nfunction retest(x) {{\n  run(x)\n}}\n"
    passes("test", "a.test.ts", head, head.replace("  run(x)", "  if (!x) {\n    return\n  }\n  run(x)"))


VERIFY = ('    "verify": "tsr generate && npm run --silent migrations:check && oxfmt --check && effect-tsgo oxlint --type-aware && '
          'effect-tsgo tsc -p tsconfig.json && effect-tsgo tsrs -p tsconfig.json && vitest run --passWithNoTests"')


@t
def a_pass_anyway_word_counts_as_added_only_when_the_file_holds_more_of_it_than_at_head():
    pkg = f'{{\n  "scripts": {{\n{VERIFY},\n    "test": "vitest run"\n  }}\n}}\n'
    passes("shared", "package.json", pkg, pkg.replace('--passWithNoTests"', '--passWithNoTests && npm run build"'))
    denies("shared", "package.json", pkg, pkg.replace('"test": "vitest run"', '"test": "vitest run --passWithNoTests"'), "stops tests from running")
    py = '[tool.pytest.ini_options]\naddopts = "--deselect tests/test_a.py::test_x"\n'
    passes("shared", "pyproject.toml", py, py.replace('addopts = "', 'addopts = "-q '))
    denies("shared", "pyproject.toml", py, py.replace('test_x"', 'test_x --deselect tests/test_b.py::test_y"'), "stops tests")
    ci = "jobs:\n  lint:\n    continue-on-error: true\n"
    denies("config", ".github/workflows/ci.yml", ci, ci + "  test:\n    continue-on-error: true\n", "stops tests from running")
    denies("config", ".husky/pre-commit", "npm run lint || true\n", "npm run lint || true\nnpm test || true\n", "stops tests from running")


@t
def lost_lines_names_every_head_line_an_edit_loses_and_minus_takes_lines_out_as_a_multiset():
    head = "a\nb\nc\nd\n"
    lost = lambda now: [x for _, x in tk.lost_lines(head, now)]  # noqa: E731
    assert lost("a\nc\n") == ["b", "d"]
    assert lost(head + "e\n") == []
    assert gt.minus(lost("a\nc\n"), {"b": 1, "d": 1}) == []
    assert gt.minus(lost("a\nc\n"), {"b": 1}) == ["d"]
    assert gt.minus(["x", "x", "y"], ["x"]) == ["x", "y"]
    assert tk.lost_lines(head, "a\nc\n") == [(2, "b"), (4, "d")]


@t
def an_approved_loss_of_a_repeated_line_leaves_no_loss_where_removing_it_from_head_would_report_one():
    head = "A\n})\nB\n})\n"
    gone = lambda now: [x for _, x in tk.align(head, now).gone]  # noqa: E731
    assert gt.minus(gone("A\n})\nB\n"), {"})": 1}) == []
    assert gt.minus(gone("A\nB\n"), {"})": 1}) == ["})"]


@t
def the_head_line_rule_judges_only_what_this_edit_loses_counting_a_repeated_line():
    head = "x()\nx()\ny()\n"
    f = lambda nxt, had: gt.findings("test", "a.test.ts", head, nxt, False, had)  # noqa: E731
    assert f("x()\ny()\nz()\n", ["x()"]) is None
    assert f("y()\n", ["x()"]).line == "x()"
    assert f("x()\n", ["x()"]).line == "y()"
    assert "changes or removes" in f("x()\n", ["x()"]).what


@t
def an_opened_path_skips_the_head_line_rule_and_keeps_every_content_rule():
    changed = PY.replace("    assert send() == 1", "    assert send() == 2")
    assert gt.findings("test", "test_a.py", PY, changed, True) is None
    assert "changes or removes" in finding("test", "test_a.py", PY, changed)
    assert "skips the HEAD test `def test_mute():`" in finding("test", "test_a.py", PY, changed.replace("def test_mute", "@pytest.mark.skip\ndef test_mute"), opened=True)
    assert "exits the test process" in finding("test", "test_a.py", PY, f"{changed}\nsys.exit(0)\n", opened=True)
    assert "stops tests from running" in finding("config", ".github/workflows/ci.yml", CI, CI.replace("npm test", "npm test || true"), opened=True)
    assert gt.findings("test", "test_a.py", PY, PY.replace("def test_sends():\n    assert send() == 1\n", ""), True) is None


@t
def a_skip_marker_below_a_lost_line_still_applies_to_its_head_test():
    nxt = PY.replace("    assert send() == 1", "    assert send() == 2").replace("def test_mute", "@pytest.mark.skip\ndef test_mute")
    assert "skips the HEAD test" in finding("test", "test_a.py", PY, nxt, opened=True)


WF = L("jobs:", "  test:", "    steps:", "      - uses: actions/checkout@v3",
       "      - uses: pnpm/action-setup@a3252b78c470c02df07e9d59298aecedc3ccdd6d # v3.0.0", "      - run: npm test")


@t
def a_workflow_step_that_only_changes_its_action_ref_keeps_the_head_line():
    passes("config", ".github/workflows/ci.yml", WF, WF.replace("checkout@v3", "checkout@v4"))
    passes("config", ".github/workflows/ci.yml", WF, WF.replace("@a3252b78c470c02df07e9d59298aecedc3ccdd6d # v3.0.0", "@fe02b34f77f8bc703788d5817da081398fad5dd2 # v4.0.0"))
    passes("config", "/repo/.github/workflows/ci.yml", WF, WF.replace("checkout@v3", "checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2"))


@t
def a_workflow_step_with_a_new_action_name_or_a_removed_step_is_refused_a_ref_change_outside_workflows_is_refused():
    denies("config", ".github/workflows/ci.yml", WF, WF.replace("actions/checkout@v3", "evil/checkout@v3"), "changes or removes a line")
    denies("config", ".github/workflows/ci.yml", WF, WF.replace("      - uses: actions/checkout@v3\n", ""), "changes or removes a line")
    denies("config", ".pre-commit-config.yaml", WF, WF.replace("checkout@v3", "checkout@v4"), "changes or removes a line")
    denies("config", ".husky/pre-commit", WF, WF.replace("checkout@v3", "checkout@v4"), "changes or removes a line")


@t
def a_project_s_extra_folders_names_and_shared_files_widen_the_kinds():
    cfg = gt.Config("full", ["checks"], [r"\.check\.py$", r"^spec/"], ["Makefile", "build/ci.cfg"])
    assert cfg.kind_of("checks/h.py") == "test" and K("checks/h.py") is None
    assert cfg.kind_of("a.check.py") == "test" and cfg.kind_of("spec/a.rb") == "test" and cfg.kind_of("lib/spec/a.rb") is None
    assert cfg.kind_of("Makefile") == "shared" and cfg.kind_of("sub/Makefile") == "shared"
    assert cfg.kind_of("build/ci.cfg") == "shared" and cfg.kind_of("other/ci.cfg") is None
    assert cfg.maybe_guarded("/r/anything.rb") and not cfg.maybe_guarded("/r/anything.rb") is False
    assert gt.Config("nonsense").mode == "off"


# ---- the hook, as a subprocess ----

class Out:
    def __init__(self, r):
        self.rc, self.stdout, self.err = r.returncode, r.stdout, r.stderr
        self.json = json.loads(r.stdout) if r.stdout.strip() else None
        spec = (self.json or {}).get("hookSpecificOutput", {})
        self.decision = spec.get("permissionDecision") or (self.json or {}).get("decision")
        self.reason = spec.get("permissionDecisionReason") or (self.json or {}).get("reason") or ""


class Project:
    """A throwaway repository with the hook scripts and guard_tests.json copied to .claude/hooks, as Setup leaves them."""

    def __init__(self, files=None, mode="full", cfg=None, repo=True, commit=True, nest="", raw_config=None):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="guard-"))
        self.root = os.path.join(self.base, nest) if nest else self.base
        self.state = tempfile.mkdtemp(prefix="guard-state-")
        os.makedirs(self.root, exist_ok=True)
        if repo:
            self.git("init", "-q", "-b", "main")
        for rel, text in (files or {}).items():
            self.disk(rel, text)
        if repo and commit and files:
            self.git("add", "-A")
            self.git("commit", "-q", "-m", "c1")
        self.hooks = os.path.join(self.root, ".claude", "hooks")
        os.makedirs(self.hooks)
        for name in ("guard_tests.py", "tests_kept.py"):
            shutil.copy(os.path.join(HERE, name), self.hooks)
        if raw_config is not None:
            self.disk(".claude/hooks/guard_tests.json", raw_config)
        elif mode is not None:
            self.disk(".claude/hooks/guard_tests.json", json.dumps(dict(cfg or {}, mode=mode)))
        self.sid, self.n = "s1", 0

    def close(self):
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.state, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def path(self, rel):
        return rel if os.path.isabs(rel) else os.path.join(self.root, rel)

    def git(self, *args):
        r = subprocess.run(["git", *args], cwd=self.root, env=ENV, capture_output=True, text=True)
        assert r.returncode == 0, f"git {' '.join(args)}: {r.stderr}"
        return r.stdout

    def disk(self, rel, text):
        full = self.path(rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)

    def read(self, rel):
        with open(self.path(rel)) as f:
            return f.read()

    def run(self, event, env=None, sid=None):
        ev = dict(session_id=sid or self.sid, cwd=self.root, transcript_path="/t", permission_mode="default", **event)
        e = dict(ENV, TMPDIR=self.state, CLAUDE_PROJECT_DIR=self.root, **(env or {}))
        return Out(subprocess.run([sys.executable, "-I", os.path.join(self.hooks, "guard_tests.py")], input=json.dumps(ev),
                                  cwd=self.root, env=e, capture_output=True, text=True))

    def pre(self, tool, tool_input, tid=None, **kw):
        self.n += 1
        return self.run(dict(hook_event_name="PreToolUse", tool_name=tool, tool_input=tool_input, tool_use_id=tid or f"u{self.n}"), **kw)

    def edit(self, rel, old, new, replace_all=False, **kw):
        c = dict(file_path=self.path(rel), old_string=old, new_string=new)
        return self.pre("Edit", dict(c, replace_all=True) if replace_all else c, **kw)

    def write(self, rel, content, **kw):
        return self.pre("Write", dict(file_path=self.path(rel), content=content), **kw)

    def multi(self, rel, edits, **kw):
        return self.pre("MultiEdit", dict(file_path=self.path(rel), edits=edits), **kw)

    def post(self, tid, tool="Edit"):
        return self.run(dict(hook_event_name="PostToolUse", tool_name=tool, tool_input={}, tool_response={}, tool_use_id=tid))

    def prompt(self, text, **kw):
        return self.run(dict(hook_event_name="UserPromptSubmit", prompt=text), **kw)

    def stop(self, active=False, **kw):
        return self.run(dict(hook_event_name="Stop", stop_hook_active=active, last_assistant_message="done"), **kw)

    def approve(self, rel, old, new):
        """An Edit that was asked about and ran: the hook's ask, then its PostToolUse."""
        o = self.edit(rel, old, new, tid="appr")
        assert o.decision == "ask", o.stdout
        self.disk(rel, self.read(rel).replace(old, new, 1))
        assert self.post("appr").stdout == ""


def passes_out(o):
    assert o.rc == 0 and o.stdout == "" and o.decision is None, f"wanted a pass, got {o.stdout!r} {o.err!r}"


def asks(o, *needles):
    assert o.rc == 0 and o.decision == "ask", f"wanted ask, got {o.stdout!r} {o.err!r}"
    assert o.reason.startswith("test-guard:"), o.reason
    for n in needles:
        assert n in o.reason, f"{n!r} not in {o.reason!r}"


A = "tests/a.test.ts"
A_HEAD = L("import { notify } from '../src/notify'", "", "it('sends once', () => {", "  notify()", "  expect(send).toHaveBeenCalledTimes(1)",
           "  expect(send).toHaveBeenCalledWith('hi')", "})")
WEAKEN = ("toHaveBeenCalledTimes(1)", "toHaveBeenCalled()")
NEXT_STEP = "stop and tell the user which test, the old line and why"


def project(files=None, **kw):
    return Project({A: A_HEAD, "src/app.ts": "a\n", **(files if files is not None else {})}, **kw)


@t
def a_new_it_block_added_to_a_tracked_test_passes():
    with project() as p:
        passes_out(p.edit(A, "})\n", "})\n\nit('sends nothing when muted', () => {\n  expect(send).not.toHaveBeenCalled()\n})\n"))


@t
def an_edit_that_weakens_to_have_been_called_times_1_is_asked_about_and_names_the_line_and_file():
    with project() as p:
        o = p.edit(A, *WEAKEN)
        asks(o, "expect(send).toHaveBeenCalledTimes(1)", p.path(A), "Approve to let Claude change existing lines in this file until the turn ends.",
             NEXT_STEP, f"/test-guard allow {p.path(A)}")
        assert "changes or removes a line that" in o.reason


@t
def the_ask_json_has_the_pre_tool_use_shape():
    with project() as p:
        o = p.edit(A, *WEAKEN)
        assert o.json["hookSpecificOutput"]["hookEventName"] == "PreToolUse" and list(o.json) == ["hookSpecificOutput"]


@t
def an_edit_that_removes_an_expect_line_is_asked_about():
    with project() as p:
        asks(p.edit(A, "  expect(send).toHaveBeenCalledWith('hi')\n", ""), "toHaveBeenCalledWith('hi')")


@t
def a_write_that_replaces_a_tracked_test_with_fewer_lines_is_asked_about():
    with project() as p:
        asks(p.write(A, "it('sends once', () => {\n  notify()\n})\n"), "import { notify } from '../src/notify'")


@t
def a_write_of_a_new_untracked_test_file_passes_also_in_a_folder_that_does_not_exist_yet():
    with project() as p:
        passes_out(p.write("src/foo.test.ts", "it('x', () => {})\n"))
        passes_out(p.write("e2e/new/flow.spec.ts", "x\n"))


@t
def a_multi_edit_whose_second_edit_changes_a_head_line_is_asked_about_one_that_only_adds_passes():
    with project() as p:
        asks(p.multi(A, [{"old_string": "})\n", "new_string": "})\n\nit('more', () => {})\n"},
                         {"old_string": WEAKEN[0], "new_string": WEAKEN[1]}]), WEAKEN[0])
        passes_out(p.multi(A, [{"old_string": "})\n", "new_string": "})\n\nit('more', () => {})\n"},
                               {"old_string": "it('more', () => {})", "new_string": "it('more', () => {\n  expect(1).toBe(1)\n})"}]))


@t
def an_edit_to_a_file_that_is_not_a_test_passes():
    with project() as p:
        passes_out(p.edit("src/app.ts", "a", "b"))


@t
def each_test_file_pattern_is_checked():
    paths = ["src/a.spec.js", "pkg/test_util.py", "pkg/util_test.py", "cmd/main_test.go", "test/helper.ts", "src/__tests__/x.ts", "e2e/login.ts",
             "src/__snapshots__/x.snap", "cmd/out.golden", "pkg/testdata/in.json", "pkg/conftest.py"]
    with Project({q: "keep\n" for q in paths + ["src/latest.ts", "src/contest/x.ts", "docs/testing.md"]}) as p:
        for q in paths:
            asks(p.edit(q, "keep", "gone"))
        for q in ["src/latest.ts", "src/contest/x.ts", "docs/testing.md"]:
            passes_out(p.edit(q, "keep", "gone"))


@t
def a_folder_named_like_a_test_folder_above_the_repo_root_does_not_make_a_file_a_test():
    with Project({"src/app.ts": "keep\n", A: "keep\n"}, nest="e2e/demo") as p:
        passes_out(p.edit("src/app.ts", "keep", "gone"))
        asks(p.edit(A, "keep", "gone"))


@t
def a_test_folder_inside_the_repo_is_found_from_the_repo_root():
    with Project({"tests/helpers/db.ts": "keep\n"}, nest="e2e/demo") as p:
        asks(p.edit("tests/helpers/db.ts", "keep", "gone"))


@t
def after_test_guard_allow_a_weakening_edit_passes_on_that_path_only():
    with project({"tests/b.test.ts": A_HEAD}) as p:
        o = p.prompt("/test-guard allow tests/a.test.ts")
        assert o.decision == "block" and p.path(A) in o.reason, o.stdout
        assert o.json["hookSpecificOutput"]["suppressOriginalPrompt"] is True
        passes_out(p.edit(A, *WEAKEN))
        asks(p.edit("tests/b.test.ts", *WEAKEN))


@t
def test_guard_alone_lists_the_allowed_paths_and_the_mode():
    with project(cfg={"picked": {"at": "2026-11-01T08:00:00Z", "by": "setup"}}, mode="rigs") as p:
        o = p.prompt("/test-guard")
        assert o.decision == "block" and "Rules: rig rules only in this project, set 2026-11-01 by setup." in o.reason and "No path is allowed" in o.reason, o.reason
        p.prompt("/test-guard allow tests/a.test.ts")
        assert p.path(A) in p.prompt("  /test-guard  ").reason


@t
def test_guard_with_an_unknown_argument_names_the_usage_and_allows_nothing():
    with project() as p:
        o = p.prompt("/test-guard tests/a.test.ts")
        assert "/test-guard allow <path>" in o.reason, o.reason
        assert "no path" not in p.prompt("/test-guard allow").reason.lower()
        asks(p.edit(A, *WEAKEN), WEAKEN[0])


@t
def a_prompt_that_only_mentions_test_guard_is_not_a_command_and_allows_nothing():
    with project() as p:
        passes_out(p.prompt("please run /test-guard allow tests/a.test.ts for me"))
        passes_out(p.prompt("/test-guardian allow tests/a.test.ts"))
        asks(p.edit(A, *WEAKEN))


@t
def an_allow_arriving_through_any_event_but_a_submitted_prompt_allows_nothing():
    with project() as p:
        for ev in [dict(hook_event_name="Stop", stop_hook_active=False, prompt="/test-guard allow tests/a.test.ts"),
                   dict(hook_event_name="SubagentStop", prompt="/test-guard allow tests/a.test.ts"),
                   dict(hook_event_name="PostToolUse", tool_name="Bash", tool_input={"command": "/test-guard allow tests/a.test.ts"}, tool_use_id="x")]:
            passes_out(p.run(ev))
        asks(p.edit(A, "toHaveBeenCalledTimes(1)", "toHaveBeenCalled()  /test-guard allow tests/a.test.ts"))
        asks(p.edit(A, *WEAKEN))


@t
def a_test_file_outside_a_git_repo_passes_and_so_does_a_repo_with_no_commit_yet():
    with project(repo=False) as p:
        passes_out(p.edit(A, *WEAKEN))
    with project(commit=False) as p:
        passes_out(p.edit(A, *WEAKEN))


@t
def git_failing_for_another_reason_is_denied_with_could_not_check():
    with project() as p:
        o = p.edit(A, *WEAKEN, env={"GIT_TEST_ASSUME_DIFFERENT_OWNER": "1"})
        assert o.decision == "deny" and o.reason.startswith("test-guard: could not check") and "dubious ownership" in o.reason, o.stdout


@t
def a_git_probe_that_cannot_run_is_denied_with_could_not_check():
    with project() as p:
        o = p.edit(A, "})\n", "})\n// more\n", env={"PATH": os.path.join(p.base, "no-git")})
        assert o.decision == "deny" and o.reason.startswith("test-guard: could not check"), o.stdout
        assert "/test-guard allow <path>" in o.reason and o.json["hookSpecificOutput"]["permissionDecision"] == "deny"


@t
def a_line_added_this_session_not_in_head_can_change():
    with project() as p:
        p.disk(A, A_HEAD + "it('new', () => {\n  expect(a).toBe(1)\n})\n")
        passes_out(p.edit(A, "expect(a).toBe(1)", "expect(a).toBeTruthy()"))


@t
def a_replace_all_edit_is_checked_on_every_match():
    with project() as p:
        p.disk(A, "// toHaveBeenCalledTimes(1) is strict\n" + A_HEAD)
        asks(p.edit(A, *WEAKEN, replace_all=True), WEAKEN[0])


@t
def removing_a_blank_head_line_passes():
    with project() as p:
        passes_out(p.write(A, A_HEAD.replace("\n\n", "\n")))


@t
def a_relative_path_resolves_against_the_session_cwd():
    with project() as p:
        asks(p.pre("Edit", {"file_path": A, "old_string": WEAKEN[0], "new_string": WEAKEN[1]}), WEAKEN[0])


@t
def a_tool_other_than_edit_multi_edit_or_write_is_left_alone():
    with project() as p:
        passes_out(p.pre("Bash", {"command": "sed -i 's/Times(1)/()/' tests/a.test.ts"}))
        passes_out(p.pre("Read", {"file_path": p.path(A)}))
        passes_out(p.run(dict(hook_event_name="Notification", message="x")))
        passes_out(p.run(dict(hook_event_name="SessionStart")))


@t
def an_edit_whose_old_string_is_not_in_the_file_or_whose_file_is_missing_passes_to_the_tool():
    with project() as p:
        passes_out(p.edit(A, "not there", "x"))
        passes_out(p.edit("tests/missing.test.ts", "a", "b"))


@t
def a_hook_body_that_throws_gives_a_deny():
    with project() as p:
        o = p.pre("Edit", {"file_path": p.path(A), "old_string": None, "new_string": "x"})
        assert o.decision == "deny" and o.reason.startswith("test-guard: could not check"), o.stdout
        o = p.pre("Write", {"file_path": p.path(A)})
        assert o.decision == "deny", o.stdout


@t
def malformed_input_gives_no_output_and_exit_0():
    with project() as p:
        for raw in ["", "not json", "[]", "null"]:
            r = subprocess.run([sys.executable, "-I", os.path.join(p.hooks, "guard_tests.py")], input=raw, env=ENV, capture_output=True, text=True)
            assert r.returncode == 0 and r.stdout == "", (raw, r.stdout, r.stderr)


@t
def an_edit_that_adds_a_skip_marker_above_a_head_test_is_asked_about_with_the_exit_text():
    with Project({"tests/test_send.py": "def test_sends():\n    assert send() == 1\n"}) as p:
        o = p.edit("tests/test_send.py", "def test_sends", "@pytest.mark.skip\ndef test_sends")
        asks(o, "@pytest.mark.skip", "skips the HEAD test", NEXT_STEP)


@t
def a_write_of_a_new_conftest_at_the_repo_root_that_patches_the_report_is_asked_about_one_with_fixtures_passes():
    with Project({"src/a.py": "a\n"}) as p:
        asks(p.write("conftest.py", 'def pytest_runtest_makereport(item, call):\n    rep.outcome = "passed"\n'), "rewrites the test report")
        passes_out(p.write("conftest.py", "import pytest\n\n@pytest.fixture\ndef db():\n    return {}\n"))


@t
def an_edit_that_drops_the_test_step_of_a_tracked_workflow_is_asked_about_a_file_named_like_one_elsewhere_passes():
    with Project({".github/workflows/ci.yml": CI, "docs/ci.yml": CI}) as p:
        asks(p.edit(".github/workflows/ci.yml", "      - run: npm test\n", ""), "run: npm test")
        passes_out(p.edit("docs/ci.yml", "      - run: npm test\n", ""))


@t
def a_snapshot_or_golden_file_keeps_its_head_lines():
    with Project({"src/__snapshots__/a.test.ts.snap": 'exports[`a 1`] = `"hi"`;\n', "cmd/out.golden": "total: 3\n"}) as p:
        asks(p.edit("src/__snapshots__/a.test.ts.snap", '"hi"', '"bye"'), "exports[`a 1`]")
        asks(p.edit("cmd/out.golden", "total: 3", "total: 4"), "total: 3")


@t
def an_edit_that_adds_pass_with_no_tests_to_a_tracked_package_json_is_asked_about_another_script_passes():
    with Project({"package.json": PKG}) as p:
        asks(p.edit("package.json", '"jest"', '"jest",\n    "test:ci": "jest --passWithNoTests"'), "stops tests from running or from failing")
        passes_out(p.edit("package.json", '"jest"', '"jest",\n    "lint": "eslint ."'))


@t
def the_verify_line_of_a_package_json_can_change_while_it_holds_pass_with_no_tests():
    pkg = f'{{\n  "scripts": {{\n{VERIFY},\n    "test": "vitest run"\n  }}\n}}\n'
    with Project({"package.json": pkg}) as p:
        passes_out(p.edit("package.json", '--passWithNoTests"', '--passWithNoTests && npm run build"'))
        asks(p.edit("package.json", '"test": "vitest run"', '"test": "vitest run --passWithNoTests"'), "stops tests from running or from failing")


@t
def a_file_that_already_lacks_a_head_line_gets_no_ask_for_an_edit_that_adds_a_test():
    lacks = A_HEAD.replace("  expect(send).toHaveBeenCalledWith('hi')\n", "")
    with project() as p:
        p.disk(A, lacks)
        passes_out(p.edit(A, "})\n", "})\n\nit('more', () => {})\n"))


@t
def a_file_that_already_lacks_a_head_line_is_asked_about_another_head_line_and_the_reason_quotes_that_one():
    lacks = A_HEAD.replace("  expect(send).toHaveBeenCalledWith('hi')\n", "")
    with project() as p:
        p.disk(A, lacks)
        o = p.edit(A, *WEAKEN)
        asks(o, "`expect(send).toHaveBeenCalledTimes(1)`")
        assert "toHaveBeenCalledWith('hi')" not in o.reason


@t
def the_hook_only_ever_prints_one_json_object_with_ask_or_deny_never_allow():
    with project() as p:
        for o in [p.edit(A, *WEAKEN), p.edit(A, "x", "y"), p.edit("src/app.ts", "a", "b"), p.write(A, "")]:
            assert o.decision in (None, "ask", "deny"), o.stdout
            assert o.stdout == "" or o.stdout.count("\n") == 1


# ---- approved edits, the turn check, the modes ----

@t
def an_approved_edit_opens_that_file_until_the_turn_ends_then_asks_again():
    with project() as p:
        p.approve(A, *WEAKEN)
        passes_out(p.edit(A, "expect(send).toHaveBeenCalledWith('hi')", "expect(send).toHaveBeenCalled()"))
        passes_out(p.prompt("next turn"))
        asks(p.edit(A, "expect(send).toHaveBeenCalledWith('hi')", "expect(send).toHaveBeenCalled()"))


@t
def an_opened_file_keeps_every_content_rule():
    with project() as p:
        p.approve(A, *WEAKEN)
        asks(p.edit(A, "  notify()\n", "  notify()\n  process.exit(0)\n"), "exits the test process")


@t
def an_edit_that_was_asked_about_but_never_ran_opens_nothing():
    with project() as p:
        asks(p.edit(A, *WEAKEN, tid="refused"))
        asks(p.edit(A, "expect(send).toHaveBeenCalledWith('hi')", "expect(send).toHaveBeenCalled()"))
        passes_out(p.post("never-asked"))


@t
def a_post_tool_use_for_an_edit_with_no_ask_changes_nothing():
    with project() as p:
        passes_out(p.edit(A, "})\n", "})\n\nit('x', () => {})\n", tid="plain"))
        passes_out(p.post("plain"))
        asks(p.edit(A, *WEAKEN))


@t
def a_bash_sed_that_weakens_a_head_test_line_blocks_the_stop_once_naming_the_line():
    with project() as p:
        passes_out(p.prompt("go"))
        p.disk(A, A_HEAD.replace(*WEAKEN))
        o = p.stop()
        assert o.decision == "block" and list(o.json) == ["decision", "reason"], o.stdout
        assert f"{p.path(A)}: `expect(send).toHaveBeenCalledTimes(1)`" in o.reason and NEXT_STEP in o.reason, o.reason
        assert p.path(A) in o.err
        passes_out(p.stop())


@t
def a_test_file_deleted_in_the_turn_blocks_the_stop():
    with project() as p:
        p.prompt("go")
        os.remove(p.path(A))
        assert p.path(A) in p.stop().reason


@t
def a_turn_that_only_adds_test_lines_or_changes_source_passes():
    with project() as p:
        p.prompt("go")
        p.disk(A, A_HEAD + "it('more', () => {})\n")
        p.disk("src/app.ts", "b\n")
        passes_out(p.stop())


@t
def a_loss_that_was_there_when_the_turn_started_is_not_blamed_on_the_turn():
    with project() as p:
        p.disk(A, "it('sends once', () => {\n})\n")
        p.prompt("go")
        passes_out(p.stop())


@t
def a_commit_in_the_turn_keeps_the_turn_start_head_as_the_base():
    with project() as p:
        p.prompt("go")
        p.disk(A, A_HEAD.replace(*WEAKEN))
        p.git("commit", "-q", "-am", "weaker")
        assert WEAKEN[0] in p.stop().reason


@t
def a_checkout_to_another_line_of_history_compares_with_the_new_head():
    with project() as p:
        p.git("checkout", "-q", "-b", "alt")
        p.disk(A, "it('other', () => {})\n")
        p.git("commit", "-q", "-am", "other")
        p.git("checkout", "-q", "main")
        p.disk("src/app.ts", "b\n")
        p.git("commit", "-q", "-am", "main moves")
        p.prompt("go")
        p.git("checkout", "-q", "alt")
        passes_out(p.stop())


@t
def an_allowed_path_is_not_reported():
    with project() as p:
        p.prompt("/test-guard allow tests/a.test.ts")
        p.prompt("go")
        os.remove(p.path(A))
        passes_out(p.stop())


@t
def outside_a_repo_or_when_git_cannot_run_the_stop_passes():
    with project(repo=False) as p:
        p.prompt("go")
        os.remove(p.path(A))
        passes_out(p.stop())
    with project() as p:
        p.prompt("go")
        os.remove(p.path(A))
        o = p.stop(env={"PATH": os.path.join(p.base, "no-git")})
        assert o.rc == 0 and o.decision is None and "could not compare" in o.err, (o.stdout, o.err)
        assert p.path(A) in p.stop().reason


@t
def a_subagent_stop_does_not_run_the_turn_check_and_a_stop_hook_active_stop_passes():
    with project() as p:
        p.prompt("go")
        os.remove(p.path(A))
        passes_out(p.run(dict(hook_event_name="SubagentStop", stop_hook_active=False, agent_id="a1", agent_type="Explore")))
        passes_out(p.stop(active=True))
        assert p.path(A) in p.stop().reason


@t
def a_workflow_that_loses_its_test_step_in_the_turn_blocks_the_stop():
    with Project({".github/workflows/ci.yml": CI}) as p:
        p.prompt("go")
        p.disk(".github/workflows/ci.yml", "jobs:\n  test:\n    steps:\n")
        assert f"{p.path('.github/workflows/ci.yml')}: `- run: npm test`" in p.stop().reason


@t
def a_loss_through_bash_still_blocks_the_stop_when_no_approved_edit_lost_that_line():
    with project() as p:
        p.prompt("go")
        asks(p.edit(A, *WEAKEN))
        p.disk(A, A_HEAD.replace(*WEAKEN))
        assert f"{p.path(A)}: `expect(send).toHaveBeenCalledTimes(1)`" in p.stop().reason


@t
def a_loss_an_approved_edit_made_is_not_reported_at_the_turn_end_but_a_later_bash_loss_is():
    with project() as p:
        p.prompt("go")
        p.approve(A, *WEAKEN)
        passes_out(p.stop())
        p.prompt("again")
        os.remove(p.path(A))
        o = p.stop()
        assert o.decision == "block" and "`import { notify } from '../src/notify'`" in o.reason, o.stdout


@t
def an_approved_edit_loses_each_of_a_repeated_line_only_as_often_as_it_was_approved():
    with Project({A: "x()\nx()\ny()\n"}) as p:
        p.prompt("go")
        p.approve(A, "x()\nx()\n", "x()\n")
        passes_out(p.stop())
        p.prompt("next")
        passes_out(p.stop())
        p.disk(A, "y()\n")
        assert "`x()`" in p.stop().reason


@t
def the_stop_names_a_loss_once_even_when_the_next_stop_is_not_a_stop_hook_continuation():
    with project() as p:
        p.prompt("go")
        os.remove(p.path(A))
        assert p.stop().decision == "block"
        passes_out(p.stop())


@t
def rigs_mode_a_changed_head_line_passes_a_skip_is_asked_about_and_a_bash_loss_passes_the_stop():
    with Project({"tests/test_b.py": "def test_b():\n    assert b() == 1\n", A: A_HEAD}, mode="rigs") as p:
        passes_out(p.edit(A, *WEAKEN))
        asks(p.edit("tests/test_b.py", "def test_b", "@pytest.mark.skip\ndef test_b"))
        p.prompt("go")
        os.remove(p.path(A))
        passes_out(p.stop())


@t
def full_mode_a_changed_head_line_is_asked_about():
    with project(mode="full") as p:
        asks(p.edit(A, *WEAKEN))


@t
def no_config_off_or_an_unreadable_config_means_every_edit_passes_and_nothing_is_written():
    for kw in [dict(mode=None), dict(mode="off"), dict(raw_config="{not json"), dict(raw_config='{"mode": "strict"}'), dict(raw_config="[]"),
               dict(raw_config='{"mode": "full", "extra_test_names": ["("]}')]:
        with project(**kw) as p:
            for o in [p.edit(A, *WEAKEN), p.edit(A, "  notify()\n", "  notify()\n  process.exit(0)\n"), p.write(".claude/settings.json", "{}"),
                      p.edit(".claude/hooks/guard_tests.py", "a", "b")]:
                assert o.rc == 0 and o.decision is None and o.stdout == "", (kw, o.stdout)
            p.prompt("go")
            os.remove(p.path(A))
            passes_out(p.stop())
            assert not os.path.exists(os.path.join(p.state, "claude-hooks", "s1", "guard-tests.json")), kw


@t
def an_unreadable_config_says_so_on_stderr():
    with project(raw_config="{not json") as p:
        assert "could not read guard_tests.json" in p.edit(A, *WEAKEN).err


@t
def extra_test_dirs_names_and_shared_files_come_from_the_config():
    cfg = {"extra_test_dirs": ["checks"], "extra_test_names": [r"\.check\.py$"], "shared_files": ["Makefile"]}
    files = {"checks/h.py": "a = 1\n", "lib/x.check.py": "a = 1\n", "Makefile": "test:\n\tpytest\n", "lib/plain.py": "a = 1\n"}
    with Project(files, cfg=cfg) as p:
        asks(p.edit("checks/h.py", "a = 1", "a = 2"))
        asks(p.edit("lib/x.check.py", "a = 1", "a = 2"))
        passes_out(p.edit("lib/plain.py", "a = 1", "a = 2"))
        passes_out(p.edit("Makefile", "pytest", "pytest -q"))
        asks(p.edit("Makefile", "pytest", "pytest --deselect a"), "stops tests from running")
        asks(p.write("lib/new.check.py", "import sys\nsys.exit(0)\n"), "exits the test process")
    with Project(files, cfg={}) as p:
        passes_out(p.edit("checks/h.py", "a = 1", "a = 2"))
        passes_out(p.edit("lib/x.check.py", "a = 1", "a = 2"))
        passes_out(p.edit("Makefile", "pytest", "pytest --deselect a"))


@t
def a_name_pattern_anchored_at_the_repo_root_counts_for_the_exit_rule_too():
    with Project({"lib/x.py": "a = 1\n"}, cfg={"extra_test_names": [r"^lib/x\.py$"]}) as p:
        asks(p.edit("lib/x.py", "a = 1", "a = 1\nimport sys\nsys.exit(0)"), "exits the test process")


@t
def an_edit_to_the_guard_s_own_files_asks_in_rigs_and_full_but_not_off():
    own = [".claude/hooks/guard_tests.py", ".claude/hooks/tests_kept.py", ".claude/hooks/guard_tests.json", ".claude/settings.json",
           ".claude/settings.local.json"]
    for mode in ("rigs", "full"):
        with project(files={".claude/settings.json": "{}\n", ".claude/other.json": "{}\n"}, mode=mode) as p:
            for rel in own:
                o = p.edit(rel, "a", "b") if os.path.exists(p.path(rel)) else p.write(rel, "{}\n")
                asks(o, p.path(rel), f"/test-guard allow {p.path(rel)}")
            asks(p.write(".claude/settings.json", "{}\n"))
            asks(p.multi(".claude/hooks/guard_tests.json", [{"old_string": "rigs", "new_string": "off"}]))
            passes_out(p.edit(".claude/other.json", "{}", "[]"))
            p.prompt("/test-guard allow .claude/settings.json")
            passes_out(p.edit(".claude/settings.json", "{}", "[]"))
    with project(files={".claude/settings.json": "{}\n"}, mode="off") as p:
        passes_out(p.edit(".claude/settings.json", "{}", "[]"))


@t
def the_guard_s_own_files_are_asked_about_outside_a_git_repo_too():
    with project(repo=False) as p:
        asks(p.edit(".claude/hooks/guard_tests.py", "a", "b"))


@t
def session_state_goes_under_tmpdir_and_never_in_the_project():
    with project() as p:
        before = sorted(p.git("status", "--porcelain", "-uall").split("\n"))
        p.prompt("go")
        p.prompt("/test-guard allow tests/a.test.ts")
        p.edit(A, *WEAKEN)
        p.stop()
        assert sorted(p.git("status", "--porcelain", "-uall").split("\n")) == before
        state = os.path.join(p.state, "claude-hooks", "s1", "guard-tests.json")
        with open(state) as f:
            st = json.load(f)
        assert st["allowed"] == [p.path(A)] and set(st) == {"allowed", "turn", "noted", "calls", "approved", "opened"}, st
        assert st["turn"]["root"] == p.root


@t
def session_state_is_per_session_and_a_session_id_cannot_leave_its_folder():
    with project() as p:
        p.prompt("/test-guard allow tests/a.test.ts", sid="one")
        passes_out(p.edit(A, *WEAKEN, sid="one"))
        asks(p.edit(A, *WEAKEN, sid="two"))
        p.prompt("/test-guard allow tests/a.test.ts", sid="../../escape")
        assert os.path.isfile(os.path.join(p.state, "claude-hooks", ".._.._escape", "guard-tests.json"))
        assert not os.path.exists(os.path.join(p.base, "escape"))


@t
def without_tmpdir_the_state_falls_back_to_tmp():
    sid = f"fallback-{os.getpid()}"
    folder = os.path.join("/tmp", "claude-hooks", sid)
    with project() as p:
        try:
            env = dict(ENV, CLAUDE_PROJECT_DIR=p.root)
            env.pop("TMPDIR", None)
            ev = dict(session_id=sid, cwd=p.root, hook_event_name="UserPromptSubmit", prompt="/test-guard allow tests/a.test.ts")
            r = subprocess.run([sys.executable, "-I", os.path.join(p.hooks, "guard_tests.py")], input=json.dumps(ev), cwd=p.root, env=env,
                               capture_output=True, text=True)
            assert r.returncode == 0 and os.path.isfile(os.path.join(folder, "guard-tests.json")), (r.stdout, r.stderr)
        finally:
            shutil.rmtree(folder, ignore_errors=True)


@t
def parallel_hook_calls_do_not_lose_a_state_write():
    with project() as p:
        procs = []
        for i in range(8):
            ev = dict(session_id="par", cwd=p.root, hook_event_name="UserPromptSubmit", prompt=f"/test-guard allow tests/f{i}.test.ts")
            procs.append(subprocess.Popen([sys.executable, "-I", os.path.join(p.hooks, "guard_tests.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          env=dict(ENV, TMPDIR=p.state), cwd=p.root, text=True))
            procs[-1].stdin.write(json.dumps(ev))
            procs[-1].stdin.close()
        for pr in procs:
            pr.wait()
        with open(os.path.join(p.state, "claude-hooks", "par", "guard-tests.json")) as f:
            assert len(json.load(f)["allowed"]) == 8


@t
def the_hook_runs_with_python_dash_i_from_any_folder():
    with project() as p:
        e = dict(ENV, TMPDIR=p.state)
        ev = dict(session_id="s1", cwd=p.root, hook_event_name="PreToolUse", tool_name="Edit", tool_use_id="u",
                  tool_input={"file_path": p.path(A), "old_string": WEAKEN[0], "new_string": WEAKEN[1]})
        r = subprocess.run([sys.executable, "-I", os.path.join(p.hooks, "guard_tests.py")], input=json.dumps(ev), cwd="/", env=e,
                           capture_output=True, text=True)
        assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask", (r.stdout, r.stderr)


@t
def the_settings_block_wires_all_four_events_to_the_script():
    with open(os.path.join(HERE, "guard_tests.settings.json")) as f:
        s = json.load(f)
    assert list(s) == ["hooks"] and set(s["hooks"]) == {"PreToolUse", "PostToolUse", "UserPromptSubmit", "Stop"}
    for event, groups in s["hooks"].items():
        for g in groups:
            assert g.get("matcher", "Edit|Write|MultiEdit") == "Edit|Write|MultiEdit"
            assert [h["command"] for h in g["hooks"]] == ['python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/guard_tests.py']
    assert s["hooks"]["PreToolUse"][0]["matcher"] == "Edit|Write|MultiEdit" and "matcher" not in s["hooks"]["Stop"][0]


print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
