---
name: implement
description: >
  This skill should be used when the user types "/implement" with a ticket or a spec. It builds
  one ready ticket without supervision: it gets the ticket from the tracker, trusts its answers,
  builds it in checked slices, runs review-loop on the commits and opens a PR that closes it.
  With a spec or several tickets, it starts one parallel worker per ready ticket.
disable-model-invocation: true
argument-hint: "<ticket | spec> [commit | pr | ready | merged]"
---

Arguments: `$ARGUMENTS`. A spec or several tickets: `references/orchestrate.md`, workers per
`references/claude-code.md`. One ticket: steps 1 to 7; never reopen the plan; end with proof,
not a question. A stop point word (default `pr`) sets how far it goes: `references/stop-points.md`.

1. **Tracker**: the one the project names, else inferred from the reference. Two: ask.
2. **Ticket** by URL or key; a bare number matched against a list picks the wrong item. Write
   its title and link. Two items match: ask. No reference: write the criteria and
   wait for my go.
3. **Gate** and branch per `references/ticket.md`.
4. **Trust the ticket**: open questions per `references/ticket.md`.
5. **Build** per `references/ticket.md`. Each criterion becomes a check, end-to-end when a user
   sees it. Commit each green slice; Out of Scope stays out.
6. **Review**: run `review-loop` on the commits since the base. One commit per fix; each
   finding that is not fixed goes in the PR.
7. **PR** with `create-pr`, body per `references/ticket.md`. Report the link, Decided and Needs
   you.
8. **Stop point**: `commit` ends after step 6 with no push; `ready` and `merged` go on per
   `references/stop-points.md`.
