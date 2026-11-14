#!/usr/bin/env python3
"""Checks that each mod's plugin.json repeats its marketplace entry's display fields.

The installed copy of a mod shows the fields in its own plugin.json, not the marketplace entry's.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ("displayName", "description", "author")


def main():
    errors = []
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    for entry in marketplace["plugins"]:
        if not entry["source"].startswith("./mods/"):
            continue
        path = ROOT / entry["source"] / ".claude-plugin/plugin.json"
        manifest = json.loads(path.read_text())
        for field in FIELDS:
            if manifest.get(field) != entry.get(field):
                errors.append(f"{path.relative_to(ROOT)}: {field} differs from its marketplace entry")
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
