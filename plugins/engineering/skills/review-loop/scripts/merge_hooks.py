#!/usr/bin/env python3
"""Adds a hook's settings block to a project's settings file, once.

Usage: python3 -I merge_hooks.py <project settings.json> <hook>.settings.json
Keeps every key and hook entry already there. Adds an entry under each event only when no entry
of that event runs the same command. Running it again changes nothing. Prints `added N` or
`unchanged`; exits 1 when either file is not a JSON object.
"""
import json
import os
import sys


def commands(entries):
    return {h.get("command") for e in entries for h in e.get("hooks", [])}


def merge(settings, block):
    """Returns (merged settings, number of entries added)."""
    out = dict(settings)
    hooks = {k: list(v) for k, v in out.get("hooks", {}).items()}
    added = 0
    for event, entries in block.get("hooks", {}).items():
        have = hooks.setdefault(event, [])
        for entry in entries:
            if not commands([entry]) <= commands(have):
                have.append(entry)
                added += 1
    out["hooks"] = hooks
    return out, added


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: not a JSON object")
    return data


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 1
    try:
        settings, block = load(argv[1]), load(argv[2])
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    merged, added = merge(settings, block)
    if added:
        os.makedirs(os.path.dirname(os.path.abspath(argv[1])), exist_ok=True)
        with open(argv[1], "w", encoding="utf-8") as f:
            f.write(json.dumps(merged, indent=2) + "\n")
    print(f"added {added}" if added else "unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
