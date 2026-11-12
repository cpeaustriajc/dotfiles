"""Tests for build_formats.sh. Run: python3 -I test_build_formats.py"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "build_formats.sh")
MASTER = ('<html><head><meta name="viewport" content="width=1080, height=1920"><style>'
          'html, body { margin: 0; width: 1080px; height: 1920px; }</style></head><body>'
          '<div id="root" data-width="1080" data-height="1920" data-format="9x16"></div></body></html>')


def run(*args):
    return subprocess.run(["sh", SCRIPT, *args], capture_output=True, text=True)


def master(tmp, html):
    d = os.path.join(tmp, "m"); os.makedirs(d)
    open(os.path.join(d, "index.html"), "w").write(html)
    return d


def main():
    results = []
    def check(name, ok): results.append(ok); print(("ok   " if ok else "FAIL ") + name)

    r = run("--help"); check("--help exits 0 and prints usage", r.returncode == 0 and "usage" in (r.stdout + r.stderr))
    r = run(); check("no argument exits 1 and prints usage", r.returncode == 1 and "usage" in (r.stdout + r.stderr))
    with tempfile.TemporaryDirectory() as tmp:
        m = master(tmp, "<html></html>")
        r = run(m); check("master without markers exits 1", r.returncode == 1 and "missing the expected markers" in r.stdout)
    with tempfile.TemporaryDirectory() as tmp:
        m = master(tmp, MASTER)
        r = run(m)
        ok = r.returncode == 0
        for f, w, h in (("1x1", 1080, 1080), ("16x9", 1920, 1080)):
            p = os.path.join(m + "-" + f, "index.html")
            ok = ok and os.path.exists(p) and f'data-format="{f}"' in open(p).read() and f"width: {w}px; height: {h}px" in open(p).read()
        check("good master yields 1x1 and 16x9 siblings", ok)
    n = sum(results); print(f"{n} passed, {len(results) - n} failed"); return 0 if n == len(results) else 1


sys.exit(main())
