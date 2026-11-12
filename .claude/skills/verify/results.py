#!/usr/bin/env python3
"""Reads each runner's own result lines from a feature log and gives the verdict.

Usage: python3 -I results.py <exit status> <log> [<base log>]
Prints one line, `VERIFIED: <why>`, `NOT VERIFIED: <cause>` or `BLOCKED: <cause>`; exits 0, 1 or 2.

A feature is VERIFIED only when the command exited 0, the log has at least one result line, no
result line counts a failure, more than zero passed, and no fewer passed than the same command ran
at the base (the base log, from a clean checkout of the base commit). Exit 0 with no result line
(an early exit, a runner that printed nothing) or with failures (`|| true`) is NOT VERIFIED.
An agent that can edit a runner can still print a fake result line; CI from the base branch is
the answer to that, not this file.
"""
import re
import sys

BUN_PASS = re.compile(r"^\s*(\d+) pass$")
BUN_FAIL = re.compile(r"^\s*(\d+) fail$")
SUMMARY = re.compile(r"^(\d+) passed, (\d+) failed$")  # this repo's script tests
UNITTEST_RAN = re.compile(r"^Ran (\d+) tests? in ")
UNITTEST_FAILED = re.compile(r"^FAILED \(([^)]*)\)$")
PYTEST = re.compile(r"^=+ (.*\b(?:passed|failed|error|errors)\b.*) in [\d.]+s")
STEP = re.compile(r"^\[\d+/\d+\] (✔|✘) ")  # tests/claude-owned/run.py
SELF_TEST = re.compile(r"^SELF-TEST PASSED: all (\d+) ")
CHECK_OK = re.compile(r"^(?:[\w-]+(?: [\w-]+)* ok|PASSED: .+|✔ Validation passed.*|tests kept: \d+ tests.*|canary ok: \d+ test files went red)$")
CHECK_FAILED = re.compile(r"^(?:[\w-]+(?: [\w-]+)* FAILED|FAILED\b.*|SELF-TEST FAILED.*|✘ Validation failed.*)$")


def parse(text):
    """(passed, failed, result lines) over every result line the log holds."""
    passed = failed = lines = 0
    ran = None
    for line in text.splitlines():
        line = line.rstrip()
        m = UNITTEST_FAILED.match(line)
        if m and ran is not None:
            bad = sum(int(n) for n in re.findall(r"(?:failures|errors)=(\d+)", m.group(1)))
            passed, failed, lines, ran = passed + ran - bad, failed + bad, lines + 1, None
            continue
        if line == "OK" or line.startswith("OK ("):
            if ran is not None:
                passed, lines, ran = passed + ran, lines + 1, None
            continue
        if m := UNITTEST_RAN.match(line):
            ran = int(m.group(1))
        elif m := BUN_PASS.match(line):
            passed, lines = passed + int(m.group(1)), lines + 1
        elif m := BUN_FAIL.match(line):
            failed, lines = failed + int(m.group(1)), lines + 1
        elif m := SUMMARY.match(line):
            passed, failed, lines = passed + int(m.group(1)), failed + int(m.group(2)), lines + 1
        elif m := PYTEST.match(line):
            nums = dict((k, int(n)) for n, k in re.findall(r"(\d+) (passed|failed|errors?)", m.group(1)))
            passed += nums.get("passed", 0)
            failed += nums.get("failed", 0) + nums.get("error", 0) + nums.get("errors", 0)
            lines += 1
        elif m := STEP.match(line):
            passed, failed, lines = passed + (m.group(1) == "✔"), failed + (m.group(1) == "✘"), lines + 1
        elif m := SELF_TEST.match(line):
            passed, lines = passed + int(m.group(1)), lines + 1
        elif CHECK_OK.match(line):
            passed, lines = passed + 1, lines + 1
        elif CHECK_FAILED.match(line):
            failed, lines = failed + 1, lines + 1
    return passed, failed, lines


def verdict(status, text, base_text=None):
    """(word, why): word is VERIFIED, NOT VERIFIED or BLOCKED."""
    if status == 2:
        why = next((ln.strip() for ln in reversed(text.splitlines()) if "BLOCKED" in ln), "exit 2")
        return "BLOCKED", why
    passed, failed, lines = parse(text)
    if status != 0:
        return "NOT VERIFIED", f"exit {status}, {failed} failed"
    if not lines:
        return "NOT VERIFIED", "exit 0 but no runner result line in the log"
    if failed:
        return "NOT VERIFIED", f"exit 0 but {failed} failed in the result lines"
    if not passed:
        return "NOT VERIFIED", "0 passed: zero tests ran"
    if base_text is not None:
        b_passed, b_failed, _ = parse(base_text)
        if passed < b_passed + b_failed:
            return "NOT VERIFIED", f"{passed} passed, but the same command ran {b_passed + b_failed} at the base"
        return "VERIFIED", f"{passed} passed, 0 failed (base ran {b_passed + b_failed})"
    return "VERIFIED", f"{passed} passed, 0 failed"


def main(argv):
    if len(argv) not in (2, 3) or not argv[0].lstrip("-").isdigit():
        print("usage: results.py <exit status> <log> [<base log>]", file=sys.stderr)
        return 64
    read = lambda p: open(p, encoding="utf-8", errors="replace").read()  # noqa: E731
    word, why = verdict(int(argv[0]), read(argv[1]), read(argv[2]) if len(argv) == 3 else None)
    print(f"{word}: {why}")
    return {"VERIFIED": 0, "NOT VERIFIED": 1, "BLOCKED": 2}[word]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
