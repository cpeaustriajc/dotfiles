# Tree outline

`scripts/check_tree.py` checks a tracker-neutral outline of the plan, not the tracker. Read the
tree back after writing and save it as JSON in a scratch file, with only the levels the run
touched: `shape` may omit `product` for a standalone project; `tickets` includes its project and
that project's items.

```json
{
  "product": {
    "name": "Domain marketplace",
    "status": "Confirmed",
    "out_of_scope": ["A marketplace for other TLDs"],
    "worth_it": "build: buyers abandon at register today; about three weeks to a first version",
    "features": [
      { "id": "F1", "title": "Buy a domain", "project": "Checkout" },
      { "id": "F2", "title": "Sell a domain", "project": null, "deferred": true }
    ]
  },
  "projects": [
    {
      "name": "Checkout",
      "feature": "F1",
      "spec_status": "Confirmed",
      "out_of_scope": ["Payment plans"],
      "open_questions": [],
      "requirements": [
        { "id": "R1", "text": "A logged-out visitor clicks Buy and lands on register with the domain still in the cart." },
        { "id": "R2", "text": "...", "dropped": true }
      ],
      "items": [
        {
          "id": "ACME-12",
          "title": "Logged-out buyer keeps the cart through register",
          "kind": "build",
          "requirements": ["R1"],
          "you_see": "The register page with the domain listed in the cart.",
          "checks": 3,
          "chars": 1180
        }
      ]
    }
  ]
}
```

- `status`, `spec_status`: `Draft` or `Confirmed`.
- `project`: the project's name, or `null` while the feature waits (listed as not yet shaped);
  `deferred: true` marks a feature or requirement left out of this round.
- `kind`: `build`, `bug`, `chore` or `prototype`; a prototype may sit under a Draft spec and cites
  no requirement.
- `checks`: the number of checks; `chars`: the body's length, which must stay under 1,500 once
  the quoted lines of its cited requirements are subtracted.

Run `python3 <shape>/scripts/check_tree.py <absolute path to the JSON>` (`<shape>` is this
skill's folder). Add `--launch` when the project enters Launch, so an unsliced requirement fails.
