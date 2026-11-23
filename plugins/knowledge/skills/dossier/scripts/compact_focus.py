#!/usr/bin/env python3
"""A command hook that tells the compaction summarizer what to keep.

Wire it for PreCompact (compact_reinject.settings.json has the block). The harness appends its
stdout to the compaction instructions on manual and auto compaction; a `# Compact instructions`
section in the instruction file was applied in 0 of 354 runs (anthropics/claude-code#89797).
Keep TEXT short: the harness sets no size limit, and a 2.2 MB output made auto-compaction
thrash (anthropics/claude-code#101057).
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
