#!/usr/bin/env python3
"""Tests check_test_names.py: the real files agree, and a change on one side is named."""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_test_names import GUARD, KEPT, ROOT, compare  # noqa: E402
from check_test_names import block, guard, kept  # noqa: E402

passed = failed = 0


def case(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got}, want {want}")


def run(root):
    """Runs the check's CLI with the two files read from under root."""
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "check_test_names.py"), str(root)], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


guard_text = (ROOT / GUARD).read_text()
kept_text = (ROOT / KEPT).read_text()
case("the real files agree", compare(guard_text, kept_text), [])
case("a name pattern changed in the guard is named on both sides",
     [e.split(": ")[0] for e in compare(guard_text.replace(r"\.(snap|golden)$", r"\.snap$"), kept_text)],
     [f"{KEPT}:{kept_text[:kept_text.index('TEST_NAME = [')].count(chr(10)) + 1}", f"{GUARD}:10"])
case("a folder dropped from tests_kept is named", compare(guard_text, kept_text.replace(', "testdata"', "")),
     [f"{KEPT}:{kept_text[:kept_text.index('TEST_DIR = {')].count(chr(10)) + 1}: folder missing, {GUARD} has testdata"])
case("a reordered name list is named", compare(guard_text, kept_text.replace(
    'r"(^|/)conftest\\.py$", r"\\.(snap|golden)$"', 'r"\\.(snap|golden)$", r"(^|/)conftest\\.py$"')),
    [f"{KEPT}:{kept_text[:kept_text.index('TEST_NAME = [')].count(chr(10)) + 1}: name patterns are in a different order than {GUARD}"])
case("no definition in the guard fails closed", compare("const x = 1\n", kept_text),
     [f"{GUARD}:1: no TEST_NAME and TEST_DIR definition found"])
case("no definition in tests_kept fails closed", compare(guard_text, "x = 1\n"),
     [f"{KEPT}:1: no TEST_NAME and TEST_DIR definition found"])

with tempfile.TemporaryDirectory() as tmp:
    for rel in (GUARD, KEPT):
        dest = pathlib.Path(tmp) / rel
        dest.parent.mkdir(parents=True)
        shutil.copy(ROOT / rel, dest)
    copy = pathlib.Path(tmp) / KEPT
    copy.write_text(copy.read_text().replace('"e2e", ', ""))
    code, out = run(tmp)
    case("the CLI on a changed copy exits 1 and names the folder", (code, out.startswith(f"{KEPT}:43: folder missing") and "folder missing" in out and "e2e" in out), (1, True))
code, out = run(ROOT)
case("the CLI on the real files exits 0", (code, out), (0, "test names ok"))


case("block returns the line and text from start through end", block("\n\nab]x", "a", "]"), (3, "ab"))
case("block is None when the start is missing, even if the text ends with the end", block("a]", "zz", "]"), None)
case("block is None when the end is missing", block("abc", "a", "]"), None)
case("block finds a start at the very beginning", block("abc]", "a", "]"), (1, "abc"))
case("block accepts an end found where the start is", block("a", "a", "a"), (1, ""))
case("a guard with only TEST_NAME is no definition", guard("const TEST_NAME = [/a/]\n"), None)
case("a guard with only TEST_DIR is no definition", guard("const TEST_DIR = new Set(['a'])"), None)
case("a tests_kept with only TEST_NAME is no definition", kept('TEST_NAME = [r"a")]\n'), None)
case("a tests_kept with only TEST_DIR is no definition", kept('TEST_DIR = {"a"}'), None)
case("the guard's TEST_DIR line is reported", guard(guard_text)[1][0], guard_text[:guard_text.index("const TEST_DIR")].count("\n") + 1)
case("a folder only tests_kept has is named once, on the guard side",
     compare(guard_text, kept_text.replace('"testdata"', '"testdata", "zzz"')),
     [f"{GUARD}:{guard_text[:guard_text.index('const TEST_DIR')].count(chr(10)) + 1}: folder missing, {KEPT} has zzz"])
case("a reorder in the guard is named", [e.split(": ", 1)[1] for e in compare(guard_text.replace(
    r"/(^|\/)conftest\.py$/, /\.(snap|golden)$/", r"/\.(snap|golden)$/, /(^|\/)conftest\.py$/"), kept_text)],
    [f"name patterns are in a different order than {GUARD}"])
case("one changed pattern in tests_kept is two errors, not a reorder",
     len(compare(guard_text, kept_text.replace(r'r"\.(snap|golden)$"', r'r"\.snap$"'))), 2)
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "check_test_names.py")], capture_output=True, text=True)
case("the CLI with no root argument checks the real files", (r.returncode, r.stdout.strip()), (0, "test names ok"))

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
