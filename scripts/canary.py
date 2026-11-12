#!/usr/bin/env python3
"""Proves each test runner this repo uses goes red when a test fails.

Usage: python3 -I scripts/canary.py [--self-test]

It copies the working tree to a temp repo, adds one failing test with a random name to every test
file (each mod's *.test.ts, each test_*.py, test_*.sh and *.test.sh), runs `smoke.sh tests` there,
and requires exit 1 and a `FAILED:` line that names each file (a mod by its folder). A file that
stays green has a rigged runner (an early exit, `|| true`, a conftest-style patch) or no runner at
all. tests/claude-owned/ is left out: `run.py --self-test` proves it.
--self-test rigs smoke.sh's run() with `|| true` and two test files with an early exit, and exits
1 unless the canary catches each.

It cannot catch a rig that only fires outside this copy (in CI only, say) or that spots the
injected test; the name is random to make the second harder.
"""
import argparse
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD_TEST = re.compile(r"^mods/([^/]+)/hooks/[^/]+\.test\.ts$")
PY_TEST = re.compile(r"(^|/)test_[^/]*\.py$")
SH_TEST = re.compile(r"(^|/)test_[^/]*\.sh$|\.test\.sh$")
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull, "GIT_AUTHOR_NAME": "canary",
           "GIT_AUTHOR_EMAIL": "canary@localhost", "GIT_COMMITTER_NAME": "canary", "GIT_COMMITTER_EMAIL": "canary@localhost"}


def inject(path, text, name):
    """The text with one failing test named `name`, or None when the file's style is unknown."""
    if MOD_TEST.match(path):
        return (text + f"\nimport {{ test as canaryTest, expect as canaryExpect }} from 'claude-code/testing'\n"
                f"canaryTest('{name}', () => {{ canaryExpect('{name}').toBe('green') }})\n")
    lines = text.split("\n")
    if PY_TEST.search(path):
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('if __name__ == "__main__":') and "unittest" in text:
                lines[i:i] = [f"class Canary(unittest.TestCase):", f"    def test_{name.replace('-', '_')}(self):",
                              f"        self.fail('{name}')", "", ""]
                return "\n".join(lines)
            pad = re.match(r"\s*", lines[i]).group()
            m = re.match(r'\s*print\(f"\{\w+\} passed, \{(\w+)\} failed"\)', lines[i])
            if m:
                lines[i:i] = [f"{pad}{m.group(1)} += 1", f"{pad}print('FAIL {name}')"]
                return "\n".join(lines)
            if re.match(r"\s*n = sum\(results\)", lines[i]):
                lines[i:i] = [f"{pad}results.append(False); print('FAIL {name}')"]
                return "\n".join(lines)
    if SH_TEST.search(path):
        for i in range(len(lines) - 1, -1, -1):
            m = re.match(r'echo "\$\w+ passed, \$(\w+) failed"', lines[i])
            if m:
                lines[i:i] = [f'{m.group(1)}=$(({m.group(1)} + 1)); echo "FAIL {name}"']
                return "\n".join(lines)
    return None


def target(path):
    """The text a FAILED: line must contain for this test file."""
    m = MOD_TEST.match(path)
    return f"mods/{m.group(1)}/" if m else path


def copy_tree(dest):
    files = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                           check=True, capture_output=True).stdout.decode().split("\0")
    for rel in filter(None, files):
        src = os.path.join(ROOT, rel)
        if not os.path.lexists(src):
            continue
        os.makedirs(os.path.dirname(os.path.join(dest, rel)), exist_ok=True)
        shutil.copy2(src, os.path.join(dest, rel), follow_symlinks=False)
    env = {**os.environ, **GIT_ENV}
    for args in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "-m", "canary copy"],
                 ["update-ref", "refs/remotes/origin/main", "HEAD"]):
        subprocess.run(["git", *args], cwd=dest, check=True, capture_output=True, env=env)
    return [f for f in files if f and os.path.isfile(os.path.join(dest, f))]


def run(dest, files, rig=None):
    """Findings, one line each; empty when every runner went red."""
    name = f"canary-{secrets.token_hex(4)}"
    findings, injected = [], []
    for rel in files:
        if rel.startswith("tests/claude-owned/") or not (MOD_TEST.match(rel) or PY_TEST.search(rel) or SH_TEST.search(rel)):
            continue
        p = os.path.join(dest, rel)
        try:
            with open(p, encoding="utf-8") as f:
                new = inject(rel, f.read(), name)
        except UnicodeDecodeError:
            findings.append(f"{rel}: not UTF-8 text, so canary cannot add a failing test")
            continue
        if new is None:
            findings.append(f"{rel}: canary cannot add a failing test to this file's style")
            continue
        with open(p, "w", encoding="utf-8") as f:
            f.write(new)
        injected.append(rel)
    if rig:
        rig(dest)
    r = subprocess.run(["bash", ".claude/skills/run-dotfiles/smoke.sh", "tests"], cwd=dest, capture_output=True,
                       text=True, stdin=subprocess.DEVNULL)
    failed = [ln for ln in r.stdout.splitlines() if ln.startswith("FAILED: ")]
    if r.returncode != 1:
        findings.append(f"smoke.sh tests: exit {r.returncode} with a failing test in every file; want 1")
    for rel in injected:
        if not any(target(rel) in ln for ln in failed):
            findings.append(f"{rel}: stayed green with a failing test added ({name}): no FAILED line names {target(rel)}")
    return findings, len(injected)


def rig_smoke(dest):
    p = os.path.join(dest, ".claude/skills/run-dotfiles/smoke.sh")
    text = open(p).read()
    new = re.sub(r'^run\(\) \{.*\}$', 'run() { "$@" || true; }', text, count=1, flags=re.M)
    assert new != text, "smoke.sh has no run() line to rig"
    open(p, "w").write(new)


def rig_exits(files):
    def rig(dest):
        for rel in files:
            p = os.path.join(dest, rel)
            lines = open(p).read().split("\n")
            lines.insert(1, "import sys; sys.exit(0)" if rel.endswith(".py") else "exit 0")
            open(p, "w").write("\n".join(lines))
    return rig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true", help="rig copies and require the canary to catch each rig")
    args = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="canary-")
    try:
        if not args.self_test:
            files = copy_tree(os.path.join(tmp, "repo"))
            findings, n = run(os.path.join(tmp, "repo"), files)
            for f in findings:
                print(f)
            print(f"canary FAILED: {len(findings)} findings" if findings else f"canary ok: {n} test files went red")
            return 1 if findings else 0
        bad = 0
        files = copy_tree(os.path.join(tmp, "a"))
        findings, n = run(os.path.join(tmp, "a"), files, rig_smoke)
        caught = sum("stayed green" in f for f in findings)
        if caught != n or not any(f.startswith("smoke.sh tests: exit 0") for f in findings):
            print(f"SELF-TEST FAILED: smoke.sh run() rigged with || true, but {caught} of {n} files and the exit were caught")
            bad = 1
        py = next(f for f in files if PY_TEST.search(f) and not f.startswith("tests/"))
        sh = next(f for f in files if SH_TEST.search(f))
        files_b = copy_tree(os.path.join(tmp, "b"))
        findings, _ = run(os.path.join(tmp, "b"), files_b, rig_exits([py, sh]))
        green = sorted(f.split(":")[0] for f in findings if "stayed green" in f)
        if green != sorted([py, sh]):
            print(f"SELF-TEST FAILED: early exits in {py} and {sh}, but the canary reported {green or 'none'}")
            bad = 1
        if not bad:
            print(f"SELF-TEST PASSED: all {n + 3} rigs caught (|| true in run() on {n} files and the exit, early exits in 2 files)")
        return bad
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
