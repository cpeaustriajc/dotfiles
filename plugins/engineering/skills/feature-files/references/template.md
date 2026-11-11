# Feature file template

Read this when you write or rewrite a feature file.

```markdown
# Checkout

**What exists**: cart, guest and signed-in checkout, test-mode card payment, receipt page.
**How a user gets there**: search → domain card → "Buy" → /cart → "Checkout".
**How to drive it**: test account from the project's test setup; test card 4242…; start URL.
**Code**: `src/checkout/`, `api/orders.ts`, `components/Cart*`.
**Tests**: `e2e/checkout.spec.ts`, `src/checkout/*.test.ts`.
**Check**: the exact command or steps that prove it works, and what to capture as evidence.
**Paths to cover**: success, cancel, payment declined, empty cart, reload mid-payment, back
after paying.
**What tends to break**: cart lost after login redirect; double charge on double click.
```

- Keep it under about 40 lines.
- Describe behaviour a user can see, not implementation.
- Each step pairs an action with a visible end state, such as reopening the saved item; a toast
  alone is not proof.
- No dates, statuses, ticket numbers or "fixed in…" notes: they go stale. The tracker and git
  history hold them.
- No build or launch steps: they live in the harness's run recipe.
