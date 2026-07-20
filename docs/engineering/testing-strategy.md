# Testing Strategy

## Goal

Tests provide fast, trustworthy evidence that critical marketplace behavior works and stays compatible. Test business risk, not framework internals.

## Test Layers

| Layer | Purpose | Examples |
| --- | --- | --- |
| Unit | Fast business-rule feedback | price calculation, order transitions, coupon eligibility |
| Integration | Real framework/database behavior | repositories, constraints, permissions, DRF serializers/views |
| Contract | Compatibility between modules and Nuxt/DRF | OpenAPI schema, error envelopes, event payloads |
| End-to-end | Critical user journeys | sign-in, browse, cart, checkout, payment callback, refund |
| Non-functional | System safety under stress | migration rehearsal, concurrency, security scans, load tests |

## Minimum Coverage by Change Type

- **Pure domain rule:** unit tests for valid, invalid, boundary, and state-transition cases.
- **DRF endpoint:** integration tests for authentication, authorization, validation, status codes, error codes, and persistence effects.
- **Nuxt feature:** component/composable tests for UI state; browser test for a changed critical journey.
- **Public contract:** schema or consumer contract test, including backward compatibility.
- **Money, stock, order, or webhook change:** idempotency, duplicate delivery, concurrency, retry, and compensation tests.
- **Migration:** forward migration, rollback/restore plan, and production-like data-volume rehearsal before release.

## Test Data Rules

- Factories/builders create explicit test data; fixtures are small and readable.
- Never use production personal data in local or CI environments.
- Generate unique identifiers and isolate database state per test.
- Test time, currency, and timezone boundaries explicitly.

## Critical Journey Suite

The release suite eventually must cover:

1. Registration/sign-in/session refresh/sign-out.
2. Catalog browse, filter, product variant selection, and media display.
3. Cart add/update/remove and persisted cart behavior.
4. Checkout price and inventory validation, order creation, and duplicate-submit protection.
5. Payment-provider success, failure, retry, and signed webhook handling.
6. Order cancellation/refund and inventory/payment reconciliation.

## Quality Rules

- A test must fail for the defect it claims to prevent.
- Do not use coverage percentage as a merge target by itself. Track critical-path coverage and mutation/defect escape trends when the suite matures.
- Quarantined/flaky tests are incidents: assign an owner and expiry date.
- A failing test blocks merge unless an explicit, time-bound exception is approved.

## Current Commands

```powershell
# Backend: run from aliexpress-api/aliexpressapi
uv sync --group dev
uv run ruff check .
uv run pytest

# Frontend: run from aliexpress-nuxt4
pnpm install
pnpm typecheck
pnpm test:run
pnpm build
```

The GitHub Actions workflow in `.github/workflows/quality.yml` runs these backend and frontend checks on pull requests and pushes to `main`.

## Current Backend Coverage

`aliexpress-api/aliexpressapi/tests/integration/test_auth_and_permissions.py` covers registration and verification-gated login, public-versus-protected route access, authenticated cart add/increment validation, and transactional checkout. Cart and checkout commands use Pydantic to reject malformed UUIDs, invalid quantities, unexpected fields, and missing idempotency keys before they reach application services. Checkout coverage verifies current-price snapshots, inventory reservation, retry replay, stock conflicts, buyer-scoped idempotency, and atomic `order.created` outbox persistence. `tests/integration/test_outbox_dispatcher.py` verifies successful publish state changes, bounded retries, and expired-lease recovery. Expand this suite alongside each endpoint; it is a starting safety net, not complete marketplace coverage.

## Next Tooling Additions

Add browser tests for the critical journey suite, OpenAPI-to-TypeScript contract validation, coverage reporting, dependency/security scanning, and performance tests as the associated features mature.
