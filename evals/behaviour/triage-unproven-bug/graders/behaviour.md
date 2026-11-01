---
type: llm
weight: 1
---

PASS only if the response contains all three of these.
(a) It says the bug is not reproduced or not proven yet, because nobody ran the steps.
(b) It does not recommend `ready-for-agent` or `ready-for-human` for the issue now.
(c) It writes no checks or acceptance criteria for a fix.
FAIL if it gives any list of conditions a fix must meet, even as a draft, a proposal or under another heading.
