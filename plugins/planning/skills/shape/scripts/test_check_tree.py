#!/usr/bin/env python3
"""Re-runnable check of check_tree.py: each case bends a good tree one way and asserts on the problems."""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_tree import check  # noqa: E402

GOOD = {
    "product": {
        "status": "Confirmed",
        "out_of_scope": ["A marketplace for other TLDs"],
        "worth_it": "build: shop owners lose domains monthly; two weeks to a first version",
        "features": [
            {"id": "F1", "title": "Buy", "project": "Checkout"},
            {"id": "F2", "title": "Sell", "project": None, "deferred": True},
        ],
    },
    "projects": [{
        "name": "Checkout", "feature": "F1", "spec_status": "Confirmed",
        "out_of_scope": ["Payment plans"], "open_questions": [],
        "requirements": [{"id": "R1", "text": "a"}, {"id": "R2", "text": "b"}],
        "items": [
            {"id": "A", "kind": "build", "requirements": ["R1"], "you_see": "cart", "checks": 3, "chars": 900},
            {"id": "B", "kind": "build", "requirements": ["R2"], "you_see": "error", "checks": 4, "chars": 1200},
        ],
    }],
}

passed = failed = 0


def case(name, bend, want, launch=False):
    global passed, failed
    tree = copy.deepcopy(GOOD)
    bend(tree)
    problems, _ = check(tree, launch)
    text = "\n".join(problems)
    ok = (not problems) if want is None else want in text
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {problems or 'no problems'}")


P = lambda t: t["projects"][0]  # noqa: E731
I = lambda t, n=0: P(t)["items"][n]  # noqa: E731


def setp(**kw):
    return lambda t: P(t).update(kw)


def seti(**kw):
    return lambda t: I(t).update(kw)


case("a good tree passes", lambda t: None, None)
case("a feature not yet shaped is only a note",
     lambda t: t["product"]["features"][1].update(deferred=False), None)
case("a project its feature does not name fails",
     lambda t: t["product"]["features"][0].update(project="Cart"), "does not name it")
case("a Confirmed product with Worth it blank fails",
     lambda t: t["product"].update(worth_it=""), "Worth it blank")
case("a project serving no feature fails", setp(feature="F9"), "serves no feature")
case("a Confirmed spec under a Draft product fails",
     lambda t: t["product"].update(status="Draft"), "under a Draft product")
case("a project may stand alone without a product", lambda t: t.pop("product"), None)
case("an empty Out of scope on a Confirmed spec fails", setp(out_of_scope=[]), "empty Out of scope")
case("open questions on a Confirmed spec fail", setp(open_questions=["who pays?"]), "open questions")
case("a build item under a Draft spec fails",
     setp(spec_status="Draft"), "under a Draft spec")
case("a prototype item under a Draft spec passes",
     lambda t: P(t).update(spec_status="Draft", items=[{"id": "M", "kind": "prototype"}]), None)
case("an item citing nothing fails", seti(requirements=[]), "cites no requirement")
case("a chore may cite nothing", seti(kind="chore", requirements=[], you_see=""), None)
case("an item citing a missing requirement fails", seti(requirements=["R7"]), "cites R7")
case("an item citing a dropped requirement fails",
     lambda t: P(t)["requirements"][0].update(dropped=True), "R1, which was dropped")
case("a build item without a you-see line fails", seti(you_see=" "), "no 'you see'")
case("six checks fail", seti(checks=6), "split it")
case("an over-long body fails", seti(chars=1600), "1600 characters")
LONG = "A returning buyer who saved a domain to the watch list gets an email when its price drops, and the link in that email opens checkout with the domain already in the cart and the new price shown."


def acme_287(t):
    P(t)["requirements"] = [{"id": f"R{n}", "text": LONG} for n in (1, 2, 3)]
    I(t).update(requirements=["R1", "R2", "R3"], chars=1963)
    P(t)["items"].pop()


case("quoted requirement lines do not count toward the limit (acme #287)", acme_287, None)
case("an over-long body names its quoted part", seti(chars=1600), "14 of them quoted")
case("an unsliced requirement is only a note before Launch",
     lambda t: P(t)["items"].pop(), None)
case("an unsliced requirement fails at Launch",
     lambda t: P(t)["items"].pop(), "no item yet for R2", launch=True)
case("a deferred requirement passes at Launch",
     lambda t: (P(t)["items"].pop(), P(t)["requirements"][1].update(deferred=True)), None, launch=True)

case("a Confirmed product with an empty Out of scope fails",
     lambda t: t["product"].update(out_of_scope=[]), "product: Confirmed with Out of scope empty")
case("a product status other than Draft or Confirmed fails",
     lambda t: t["product"].update(status="confirmed"), "status confirmed is not Draft or Confirmed")
case("a spec status other than Draft or Confirmed fails",
     setp(spec_status="Approved"), "spec status Approved is not Draft or Confirmed")
case("an unknown item kind fails", seti(kind="story"), "kind story is not build, bug, chore or prototype")
case("a non-numeric checks count is a problem, not a crash", seti(checks="3"), "checks is not a whole number")
case("zero checks fail", seti(checks=0), "no checks")


import json  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402


def absent(name, bend, text, launch=False):
    global passed, failed
    tree = copy.deepcopy(GOOD)
    bend(tree)
    problems, _ = check(tree, launch)
    if text not in "\n".join(problems):
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {problems}")


def verdict(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got!r}, want {want!r}")


case("1500 characters is the limit and passes", seti(kind="chore", requirements=[], chars=1500), None)
case("1501 characters fail", seti(kind="chore", requirements=[], chars=1501), "1501 characters")
case("one check passes", seti(checks=1), None)
case("five checks pass", seti(checks=5), None)
case("a body is measured by subtraction of the quoted part, not xor", seti(chars=1504, requirements=["R1"]), None)
case("an item of an unknown kind still cites a requirement", seti(kind="story", requirements=[]), "cites no requirement")
case("a prototype does not end the item loop",
     lambda t: P(t).update(spec_status="Draft", items=[{"id": "M", "kind": "prototype"}, {"id": "B", "kind": "build"}]), "item B: a build item under a Draft spec")
case("a Draft product with a Confirmed spec fails", lambda t: t["product"].update(status="Draft"), "spec is Confirmed under a Draft product")
case("a product with an unknown status and a Confirmed spec fails", lambda t: t["product"].update(status="Approved"), "spec is Confirmed under a Draft product")
case("a spec with an unknown status is not Confirmed, so its items fail", setp(spec_status="Approved"), "under a Draft spec")
absent("a Draft spec under a Draft product is not a Confirmed spec", lambda t: (t["product"].update(status="Draft"), P(t).update(spec_status="Draft", items=[])), "spec is Confirmed")
absent("an unknown spec status under a Draft product is not a Confirmed spec", lambda t: (t["product"].update(status="Draft"), P(t).update(spec_status="Approved", items=[])), "spec is Confirmed")
absent("a Draft product needs no Worth it", lambda t: t["product"].update(status="Draft", worth_it="", out_of_scope=[]), "Confirmed with")
absent("an unknown product status needs no Worth it", lambda t: t["product"].update(status="Approved", worth_it="", out_of_scope=[]), "Confirmed with")
notes = check(copy.deepcopy(GOOD))[1]
verdict("a good tree has no notes", notes, [])
unsliced = copy.deepcopy(GOOD)
P(unsliced)["items"].pop()
verdict("an unsliced requirement is a note by default", check(unsliced), ([], ["project Checkout: no item yet for R2"]))
unshaped = copy.deepcopy(GOOD)
unshaped["product"]["features"][1]["deferred"] = False
verdict("an unshaped feature is a note", check(unshaped), ([], ["product: not yet shaped: F2"]))
shaped = copy.deepcopy(GOOD)
shaped["product"]["features"][1].update(project="Other", deferred=False)
verdict("a feature with a project is not waiting", check(shaped)[1], [])

DIR = os.path.dirname(os.path.abspath(__file__))


def cli(name, tree, args, code, want):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.json")
        with open(path, "w") as f:
            json.dump(tree, f)
        r = subprocess.run([sys.executable, "-I", os.path.join(DIR, "check_tree.py")] + [path if a == "FILE" else a for a in args],
                           capture_output=True, text=True)
    verdict(name, (r.returncode, r.stdout, r.stderr.startswith("usage")), (code, want, code == 2))


cli("the CLI on a good tree exits 0", GOOD, ["FILE"], 0, "tree ok\n")
bad = copy.deepcopy(GOOD)
bad["product"]["worth_it"] = ""
cli("the CLI prints a problem and exits 1, with no 'tree ok'", bad, ["FILE"], 1, "product: Confirmed with Worth it blank\n")
cli("the CLI prints a note", unshaped, ["FILE"], 0, "note: product: not yet shaped: F2\ntree ok\n")
cli("the CLI with --launch before the file fails an unsliced requirement", unsliced, ["--launch", "FILE"], 1, "project Checkout: no item yet for R2\n")
cli("the CLI with --launch after the file fails an unsliced requirement", unsliced, ["FILE", "--launch"], 1, "project Checkout: no item yet for R2\n")
cli("the CLI without --launch passes an unsliced requirement", unsliced, ["FILE"], 0, "note: project Checkout: no item yet for R2\ntree ok\n")
draft = copy.deepcopy(GOOD)
draft["product"]["status"] = "Draft"
cli("the CLI sees a Confirmed spec under a Draft product", draft, ["FILE"], 1, "project Checkout: spec is Confirmed under a Draft product\n")
cli("the CLI without a file exits 2", GOOD, [], 2, "")
cli("the CLI with two files exits 2", GOOD, ["FILE", "FILE"], 2, "")
cli("the CLI with only a flag exits 2", GOOD, ["--launch"], 2, "")
chore = copy.deepcopy(GOOD)
P(chore).update(items=[{"id": "C", "kind": "chore", "requirements": []}, {"id": "A", "kind": "build", "requirements": ["R1", "R2"], "you_see": "x", "checks": 2}])
cli("the CLI accepts a chore citing nothing", chore, ["FILE"], 0, "tree ok\n")
proto = copy.deepcopy(GOOD)
P(proto).update(spec_status="Draft", items=[{"id": "M", "kind": "prototype"}])
proto["product"]["status"] = "Draft"
cli("the CLI accepts a prototype under a Draft spec", proto, ["FILE"], 0, "tree ok\n")

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
