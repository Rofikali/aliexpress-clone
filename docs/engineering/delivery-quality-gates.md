# Delivery Quality Gates

## Pull Request Gate

Every change should have a focused description, linked acceptance criteria, and evidence for the applicable checks.

- Formatting, linting, type checking, and relevant automated tests pass.
- New or changed API/events are documented and contract-checked.
- Authorization, validation, error, and empty/loading states are covered.
- Database changes include migration safety and rollback/restore notes.
- Documentation and runbooks change with behavior or operations.

## Elevated Review Gate

Require an additional reviewer for payments, checkout, inventory, authentication, authorization, personal data, webhooks, infrastructure, secrets, database migrations, or cross-module dependencies.

## Release Gate

- Build artifacts are reproducible from lockfiles.
- Required test suites and security scans pass.
- Environment configuration, migrations, backups, monitoring, and rollback are ready.
- Dashboards and alerts for changed critical paths exist.
- Feature flags and staged rollout are used when rollback is not immediate.

## Post-Release Gate

- Verify endpoint health, error rate, latency, and business success signals.
- Reconcile payment/order/inventory state for relevant releases.
- Close the release only after the defined observation period is healthy.

## Exception Policy

An exception records the risk, compensating control, accountable owner, expiry date, and follow-up ticket. Exceptions are visible and expire; they are never a hidden way to bypass engineering discipline.
