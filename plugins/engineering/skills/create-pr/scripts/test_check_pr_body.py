#!/usr/bin/env python3
"""Re-runnable check of check_pr_body.py: each case bends a good body one way and asserts on the findings."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_pr_body import check  # noqa: E402

GOOD = """The digest now batches notifications per user, so a user gets one email an hour. SHOP-42

Evidence: ![before](./before.png) ![after](./after.png), `npm run e2e -- digest`
Merge danger: two-way door; blast radius: the digest job.
Test changes: tests kept: 41 tests, 120 assertions (base: 40, 117)

```diff
- # old -> new
+ ## Summary
```
"""

passed = failed = 0


def case(name, body, want, template=False):
    global passed, failed
    text = "\n".join(f"{n}: {c}" for n, c in check(body, template))
    ok = (not text) if want is None else want in text
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {text or 'no findings'}")


case("a good body passes, code blocks and inline code ignored", GOOD, None)
case("Closes #12 is a closing keyword", GOOD + "Closes #12\n", "closing keyword 'Closes #12'")
case("fixes: SHOP-42 is a closing keyword", GOOD + "This fixes: SHOP-42.\n", "closing keyword")
case("resolved owner/repo#3 is a closing keyword", GOOD + "resolved a/b#3\n", "closing keyword")
case("a closing keyword counts with --template too", GOOD + "Fixes #1\n", "closing keyword", True)
case("fix in plain prose passes", GOOD + "This is a fix for the digest.\n", None)
case("a heading is rejected", "## Summary\n" + GOOD, "1: heading")
case("a heading passes with --template", "## Summary\n" + GOOD, None, True)
case("a checklist item is rejected", GOOD + "- [ ] run tests\n", "checklist item")
case("a missing Test changes line is named", GOOD.replace("Test changes:", "Tests:"), "missing 'Test changes:'")
case("a missing Merge danger line is named", GOOD.replace("Merge danger:", "Danger:"), "missing 'Merge danger:'")
case("a 4-line summary is rejected", "a\nb\nc\nd\n" + GOOD, "4: summary over 3 lines")
case("a 3-line summary passes", "a\nb\n" + GOOD, None)
case("a long summary passes with --template", "a\nb\nc\nd\n" + GOOD, None, True)
case("an em dash is rejected", GOOD + "It is faster — much faster.\n", "em dash")
case("an arrow is rejected", GOOD + "login → token → retry\n", "arrow")
case("an arrow in inline code passes", GOOD + "Run `a -> b` once.\n", None)


case("a 5-line summary is one finding, at line 4", "a\nb\nc\nd\ne\n" + GOOD, "4: summary over 3 lines")
if sum("summary over" in c for _, c in check("a\nb\nc\nd\ne\n" + GOOD)) == 1:
    passed += 1
    print("ok   a 5-line summary is reported once")
else:
    failed += 1
    print("FAIL a 5-line summary is reported once")
case("a missing required line is reported at line 0", GOOD.replace("Test changes:", "Tests:"), "0: missing 'Test changes:'")
case("the default is the full check, so a heading is rejected", "## Summary\n" + GOOD, "heading")
import subprocess, tempfile  # noqa: E402,E401


def cli(name, body, args, code, want):
    global passed, failed
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "body.md")
        if body is not None:
            open(path, "w", encoding="utf-8").write(body)
        argv = [path if a == "FILE" else a for a in args]
        r = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_pr_body.py")] + argv,
                           capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode == code and want in out and not (code == 1 and "pr body ok" in out):
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: exit {r.returncode}, {out!r}")


cli("the CLI on a good body exits 0", GOOD, ["FILE"], 0, "pr body ok")
cli("the CLI names the file and line of a finding and exits 1", GOOD + "Closes #12\n", ["FILE"], 1, "body.md:")
cli("the CLI prints each finding", GOOD + "a — b\nc → d\n", ["FILE"], 1, "arrow")
cli("the CLI with --template skips the shape checks", "## Summary\n", ["FILE", "--template"], 0, "pr body ok")
cli("the CLI with --template first skips them too", "## Summary\n", ["--template", "FILE"], 0, "pr body ok")
cli("the CLI without arguments exits 2 with the usage", None, [], 2, "Usage")
cli("the CLI with two files exits 2", GOOD, ["FILE", "FILE"], 2, "Usage")
cli("the CLI with only --template exits 2", GOOD, ["--template"], 2, "Usage")
cli("the CLI on an unreadable file exits 2 and names it", None, ["FILE"], 2, "could not read")

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
