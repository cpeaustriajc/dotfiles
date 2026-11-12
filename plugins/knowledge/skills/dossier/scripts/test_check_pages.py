#!/usr/bin/env python3
"""Re-runnable check of check_pages.py: each case bends a good wiki one way and asserts on the problems."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_pages import check  # noqa: E402


def decision(n, topic, status="Accepted", date="2026-09-18", sections=("Context", "Decision", "Consequences"), extra=""):
    body = f"# Decision {n}: {topic}\n\n**Status:** {status}\n**Date:** {date} · **Issue:** none recorded\n\n"
    return body + "".join(f"## {s}\nx\n\n" for s in sections) + extra


GOOD = {
    "Home.md": "Why.\n\n| Page | What it answers |\n|---|---|\n| [[Decisions]] | log |\n| [[Pricing Research]] | prices |\n",
    "Decisions.md": "| # | Decision | Status | Date | Issue |\n|---|---|---|---|---|\n"
                    "| 002 | [[Decision 002 Tiers]] | Accepted | 2026-10-01 | none |\n"
                    "| 001 | [[Decision 001 Pricing]] | Superseded | 2026-09-18 | none |\n",
    "Pricing-Research.md": "Dated 2026-09-01.\n",
    "Decision-001-Pricing.md": decision("001", "Pricing", "Superseded by [[Decision 002 Tiers]]"),
    "Decision-002-Tiers.md": decision("002", "Tiers", date="2026-10-01"),
}


def run(**edits):
    with tempfile.TemporaryDirectory() as d:
        files = {**GOOD, **edits}
        for name, text in files.items():
            if text is not None:
                (Path(d) / name).write_text(text, encoding="utf-8")
        return check(d)


CASES = [
    ("good wiki passes", {}, None),
    ("superseded page without a link", {"Decision-001-Pricing.md": decision("001", "Pricing", "Superseded")}, "Status"),
    ("link to a missing successor", {"Decision-001-Pricing.md": decision("001", "Pricing", "Superseded by [[Decision 009 Gone]]")}, "resolves to no page"),
    ("partly superseded without the part", {"Decision-001-Pricing.md": decision("001", "Pricing", "Partly superseded by [[Decision 002 Tiers]]")}, "Status"),
    ("missing section", {"Decision-002-Tiers.md": decision("002", "Tiers", date="2026-10-01", sections=("Context", "Decision"))}, "Consequences"),
    ("missing date", {"Decision-002-Tiers.md": decision("002", "Tiers", date="soon")}, "Date"),
    ("dotted name", {"Pricing-v1.2.md": "x\n", "Home.md": GOOD["Home.md"] + "[[Pricing v1.2]]\n"}, "dot"),
    ("duplicate number", {"Decision-002-Other.md": decision("002", "Other"), "Home.md": GOOD["Home.md"]}, "already used"),
    ("research page not on Home", {"Orphan.md": "x\n"}, "does not link [[Orphan]]"),
    ("index out of order", {"Decisions.md": GOOD["Decisions.md"].replace("2026-10-01", "2026-08-01")}, "newest first"),
    ("decision with no index row", {"Decisions.md": GOOD["Decisions.md"].splitlines(True)[0] + GOOD["Decisions.md"].splitlines(True)[1] + GOOD["Decisions.md"].splitlines(True)[2]}, "no row for"),
    ("page mentions Claude", {"Pricing-Research.md": "Claude found this.\n"}, "check: mentions Claude or agents"),
    ("support agent is flagged to judge", {"Pricing-Research.md": "A support agent answers.\n"}, "judge whether"),
    ("no Home", {"Home.md": None}, "no Home"),
]

passed = failed = 0
for name, edits, want in CASES:
    got = run(**edits)
    ok = (not got) if want is None else any(want in g for g in got)
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}: {got}")

import subprocess  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_ROWS = GOOD["Decisions.md"]
CASES2 = [
    ("underscore and dot files are not pages", {"_Draft.md": "x\n", ".Hidden.md": "x\n"}, None),
    ("the duplicate number message names the number", {"Decision-002-Other.md": decision("002", "Other")}, "number 002 is already used"),
    ("the heading message names the number", {"Decision-002-Tiers.md": "# Wrong\n**Status:** Accepted\n**Date:** 2026-10-01\n## Context\n## Decision\n## Consequences\n"}, "not '# Decision 002: <Topic>'"),
    ("the status message names the bad status", {"Decision-002-Tiers.md": decision("002", "Tiers", "Maybe", "2026-10-01")}, "Status 'Maybe' is not"),
    ("a missing Status line is named", {"Decision-002-Tiers.md": decision("002", "Tiers", date="2026-10-01").replace("**Status:** Accepted\n", "")}, "no **Status:** line"),
    ("a row that does not show the status is named", {"Decisions.md": STATUS_ROWS.replace("| Accepted |", "| Proposed |")}, "row for Decision-002-Tiers does not show its Status 'accepted'"),
    ("a missing row does not stop the later rows being checked", {"Decisions.md": STATUS_ROWS.replace("| 001 | [[Decision 001 Pricing]] | Superseded | 2026-09-18 | none |\n", "").replace("| Accepted |", "| Proposed |")}, "does not show its Status"),
    ("month-only and full dates in one month are not out of order", {"Decisions.md": STATUS_ROWS.replace("2026-10-01", "2026-09").replace("2026-09-18", "2026-09-18")}, None),
]
for name, edits, want in CASES2:
    got = run(**edits)
    ok = (not got) if want is None else any(want in g for g in got)
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}: {got}")


def cli(name, args, make, code, want):
    global passed, failed
    with tempfile.TemporaryDirectory() as d:
        if make:
            for fname, text in GOOD.items():
                (Path(d) / fname).write_text(text, encoding="utf-8")
            if make == "bad":
                (Path(d) / "Orphan.md").write_text("x\n", encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", os.path.join(DIR, "check_pages.py")] + [d if a == "DIR" else a for a in args], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode == code and want in out:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}: exit {r.returncode}, {out!r}")


cli("the CLI on a good wiki exits 0", ["DIR"], "good", 0, "0 problem(s)")
cli("the CLI on a bad wiki exits 1 and lists the problem", ["DIR"], "bad", 1, "Home: does not link [[Orphan]]\n1 problem(s)")
cli("the CLI without a folder exits 1 with the usage", [], None, 1, "Usage")
cli("the CLI with two folders exits 1 with the usage", ["DIR", "DIR"], "good", 1, "Usage")

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
