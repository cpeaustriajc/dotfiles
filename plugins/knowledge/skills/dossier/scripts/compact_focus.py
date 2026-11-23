#!/usr/bin/env python3
"""Keep TEXT under 1000 characters: a 2.2 MB output made auto-compaction thrash (anthropics/claude-code#101057).
A `# Compact instructions` section is no substitute: the harness applied it in 0 of 354 runs (anthropics/claude-code#89797).
"""

TEXT = (
    "Keep every decision and intent from the whole conversation, including each one in an "
    "earlier summary. For each one, quote the user's words, or give the agent's proposal, "
    "verdict or withdrawal with its numbers, names and placement. Mark whether the user "
    "accepted it, rejected it or never answered. Keep each rule quoted from a plan or spec. "
    "Copy each instruction at the strength it had. Write nothing the conversation does not show."
)

if __name__ == "__main__":
    print(TEXT)
