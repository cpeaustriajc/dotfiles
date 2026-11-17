#!/usr/bin/env python3
"""Tests check_skill_refs.py on Markdown text and a set of files that exist."""
import os
import pathlib
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subprocess  # noqa: E402

from check_skill_refs import ROOT, dead, markdown_files, skill_root  # noqa: E402
from check_skill_refs import crossing, drifted  # noqa: E402

P = pathlib.PurePosixPath
ROOTS = [P("s/skills/x/references"), P("s/skills/x"), P("")]
FILES = {P("s/skills/x/references/a.md"), P("s/skills/x/scripts/b.py"), P("s/skills/y/SKILL.md"), P("scripts/c.py"),
         P("library/index.md")}
passed = failed = 0


def case(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got}, want {want}")


def run(text):
    return dead(text, ROOTS, lambda p: P(os.path.normpath(p)) in FILES)


case("a dead reference names its line and path", run("hi\nSee `references/gone.md`.\n"), [(2, "references/gone.md")])
case("a dead link names its line and path", run("[x](references/gone.md)"), [(1, "references/gone.md")])
case("a file next to the file passes", run("`references/a.md`"), [])
case("a file in the skill root passes", run("`scripts/b.py`"), [])
case("a file in the repo root passes", run("`scripts/c.py` and `library/index.md`"), [])
case("a sibling skill passes", run("[y](../y/SKILL.md)"), [])
case("a fragment is dropped", run("[x](references/a.md#top)"), [])
case("a backticked fragment is dropped", run("`references/a.md#top`"), [])
case("a dead file with a fragment still fails", run("[x](references/gone.md#top)"), [(1, "references/gone.md")])
case("a link with a title resolves", run('[x](references/a.md "t")'), [])
case("a placeholder passes", run("`references/<name>.md` `scripts/{a,b}.py` `scripts/$X.sh`"), [])
case("a glob passes", run("`references/*.md`"), [])
case("a URL passes", run("[x](https://example.com/a/b.md) `https://e.com/references/z.md`"), [])
case("an anchor passes", run("[x](#section)"), [])
case("an absolute path passes", run("`/etc/references/z.md` `~/scripts/z.py`"), [])
case("a user-project path passes", run("`src/app.ts` `docs/x.md` `.github/workflows/ci.yml` `AGENTS.md`"), [])
case("a code fence passes", run("```\n`references/gone.md` [x](scripts/gone.py)\n```\n"), [])
case("text after a fence is checked", run("```\nx\n```\n`references/gone.md`"), [(4, "references/gone.md")])
case("a name with no known extension passes", run("`references/gone.txt` `references/gone`"), [])

case("a skill folder is the root of its files", skill_root(ROOT / "plugins/p/skills/s/references/a.md"), ROOT / "plugins/p/skills/s")
case("a project skill folder is the root of its files", skill_root(ROOT / ".claude/skills/s/SKILL.md"), ROOT / ".claude/skills/s")
case("the checked files are found", len(list(markdown_files())) > 50, True)
r = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, "check_skill_refs.py")], capture_output=True, text=True)
case("the CLI exit code follows its output", (r.returncode, r.stdout.strip() == "skill refs ok"), (0, True) if r.returncode == 0 else (1, False))
case("the CLI findings have the path:line: names form", all(" names " in l and ", which does not exist" in l for l in r.stdout.splitlines() if r.returncode), True)

rng = random.Random(7)
alphabet = "abcdefghijklmnopqrstuvwxyz"
bad = []
for _ in range(200):
    name = "".join(rng.choice(alphabet) for _ in range(rng.randint(3, 10)))
    folder = rng.choice(["references", "scripts", "library", "assets"])
    ext = rng.choice(["md", "py", "sh", "json"])
    live = {P(f"s/skills/x/{folder}/{name}.{ext}")}
    ref = f"{folder}/{name}.{ext}"
    i = rng.randrange(len(name))
    other = rng.choice(alphabet.replace(name[i], ""))
    broken = f"{folder}/{name[:i]}{other}{name[i + 1:]}.{ext}"
    ok = dead(f"`{ref}`", ROOTS, lambda p: P(os.path.normpath(p)) in live) == []
    gone = dead(f"`{broken}`", ROOTS, lambda p: P(os.path.normpath(p)) in live) == [(1, broken)]
    if not (ok and gone):
        bad.append((ref, broken))
case("property: an existing path passes and a one-character change fails", bad, [])

import tempfile  # noqa: E402

with tempfile.TemporaryDirectory() as tmp:
    tree = pathlib.Path(tmp).resolve()

    def write(rel, text):
        f = tree / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)

    def cli_on(folder):
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, "check_skill_refs.py"), str(folder)],
                           capture_output=True, text=True)
        return r.returncode, r.stdout.strip()

    write("plugins/p/skills/s/SKILL.md", "# s\nSee `references/x.md`.\nAnd `references/y.md`.\n")
    write("plugins/p/skills/s/references/x.md", "# x\n")
    write("plugins/p/skills/t/README.md", "# m\n\n[doc](docs/gone.md)\n")
    case("the CLI reports each dead reference and exits 1", cli_on(tree),
         (1, "plugins/p/skills/s/SKILL.md:3: names references/y.md, which does not exist\n"
             "plugins/p/skills/t/README.md:3: names docs/gone.md, which does not exist"))
    clean = tree / "clean"
    write("clean/plugins/p/skills/s/SKILL.md", "# s\nSee `references/x.md`.\n")
    write("clean/plugins/p/skills/s/references/x.md", "# x\n")
    case("the CLI on a clean tree prints ok and exits 0", cli_on(clean), (0, "skill refs ok"))

    write("cross/plugins/p/skills/s/SKILL.md", "# s\nSee `../t/references/x.md`.\n")
    write("cross/plugins/p/skills/s/references/a.md", "# a\nSee `../../t/references/x.md`.\n")
    write("cross/plugins/p/skills/t/references/x.md", "# x\n")
    cross = tree / "cross"
    case("a path into another skill fails", crossing(cross / "plugins/p/skills/s/SKILL.md", "See `../t/references/x.md`.", cross),
         [(1, "../t/references/x.md")])
    case("a path into another skill from references/ fails",
         crossing(cross / "plugins/p/skills/s/references/a.md", "See `../../t/references/x.md`.", cross), [(1, "../../t/references/x.md")])
    case("a path inside the skill passes", crossing(cross / "plugins/p/skills/s/SKILL.md", "See `references/a.md`.", cross), [])
    case("a path to the repo's docs passes",
         crossing(cross / "plugins/p/skills/s/README.md", "[d](../../../../docs/a.md)", cross), [])
    code, out = cli_on(cross)
    case("the CLI reports a path into another skill and exits 1",
         (code, "plugins/p/skills/s/SKILL.md:2: names ../t/references/x.md, in another skill; copy it into this skill" in out),
         (1, True))

    write("copies/a/src.md", "same\n")
    write("copies/b/same.md", "same\n")
    write("copies/c/other.md", "changed\n")
    copies = tree / "copies"
    case("an equal copy passes", drifted(copies, {"a/src.md": ["b/same.md"]}), [])
    case("a changed copy fails", drifted(copies, {"a/src.md": ["c/other.md"]}),
         ["c/other.md: differs from a/src.md; edit the source, then copy it again"])
    case("a missing copy fails", drifted(copies, {"a/src.md": ["d/gone.md"]}), ["d/gone.md: missing copy of a/src.md"])

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
