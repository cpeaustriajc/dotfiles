#!/usr/bin/env python3
"""Tests graders_changed.py on file lists like the pull request files API returns."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graders_changed import graders  # noqa: E402

passed = failed = 0


def case(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got}, want {want}")


case("a skill change is not a grader", graders(["plugins/planning/skills/shape/SKILL.md"]), [])
case("a mod and its test are judged, not graders", graders(["mods/test-guard/hooks/register.test.ts"]), [])
for path in (".github/workflows/checks.yml", ".github/workflows/new.yml", "scripts/check_trunk.py", "scripts/canary.py",
             ".claude/skills/verify/drive.sh", ".claude/skills/run-dotfiles/smoke.sh", ".gitattributes",
             "plugins/engineering/skills/review-loop/scripts/tests_kept.py", "tests/claude-owned/run.py"):
    case(f"{path} is a grader", graders([path]), [path])
case("a look-alike path is not a grader", graders(["plugins/x/scripts/check.py", "docs/scripts/a.md", "a.gitattributes"]), [])


def cli(stdin):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "graders_changed.py")], input=stdin,
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


case("the CLI passes a list with no grader", cli("README.md\nmods/x/hooks/register.ts\n"),
     (0, "graders unchanged: 2 files checked"))
case("the CLI names each grader and exits 1", cli("README.md\nscripts/canary.py\n"),
     (1, "scripts/canary.py: changes a grader; the owner reviews the diff and merges past this check"))

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
