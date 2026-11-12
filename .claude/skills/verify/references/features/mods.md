# Mods

What exists: each `mods/<mod>/` is a plugin with a hooks module and its tests.

- **Code:** `mods/<mod>/**`; `tests/claude-owned/**` (applies to every mod)
- **Tests:** `claude plugin test mods/<mod>` for each changed mod.
- **Check:** `python3 tests/claude-owned/run.py` ends with `PASSED`.
