# Manifests and READMEs

What exists: `.claude-plugin/marketplace.json` (the only manifest of the listed plugins), the root README's
tables, and a README per skill and mod.

- **Code:** `**/.claude-plugin/**`, `README.md`, `**/README.md`, `scripts/check_readmes.py`,
  `scripts/test_check_readmes.py`
- **Tests:** `claude plugin validate .`; `smoke.sh tests` runs `scripts/check_readmes.py` and its
  tests.
- **Check:** `claude plugin validate .` exits 0; each changed manifest parses with
  `python3 -c 'import json,sys; json.load(open(sys.argv[1]))' <file>`.
