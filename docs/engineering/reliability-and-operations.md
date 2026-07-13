# Reliability and Operations

## Operational Principles

- Design for partial failure: providers, queues, databases, and networks fail independently.
- Prefer graceful degradation over data loss or incorrect financial/inventory state.
- Make failures observable, actionable, and recoverable.
- Automate routine recovery; keep human runbooks for exceptional cases.

## Critical Paths

Catalog reads, cart updates, checkout, payment webhooks, order changes, inventory reservation, and notifications require explicit failure behavior. For each path define timeout, retry policy, idempotency key, consistency expectation, audit record, and user-facing fallback.

## Observability Standard

Every service request and background job should carry a `request_id` and `correlation_id`. Emit structured logs with event name, outcome, latency, actor type, module, and safe identifiers. Add metrics for requests, errors, latency, retries, queue/outbox age, inventory conflicts, and payment outcomes.

Trace an operation across HTTP request, application use case, database transaction, outbox publication, and background consumer before introducing distributed services.

## Health and Readiness

- **Liveness:** process can run; it must not depend on a database query.
- **Readiness:** dependencies needed to safely serve traffic are available.
- **Startup validation:** settings, secrets, migrations, storage, and provider configuration are checked with actionable errors.

Do not route traffic to a process that is alive but cannot safely serve checkout or write data.

## Resilience Rules

- Timeouts are mandatory for remote calls.
- Retry only transient failures and use exponential backoff with jitter.
- Make commands and event consumers idempotent before retrying them.
- Use circuit breaking/bulkheads when external-provider failure can exhaust resources.
- Store integration events in an outbox transactionally; provide replay and dead-letter handling.
- Run database migrations using expand/contract steps and retain a tested rollback/restore path.

## SLOs and Alerts

Set initial targets only after baseline measurement. Candidate service-level indicators are API availability, p95 latency, checkout completion, payment webhook lag, outbox age, and error rate. Alerts must identify an owner, customer impact, urgency, and first diagnostic step; an alert without an action is noise.

## Incident Loop

1. Stabilize users and preserve data.
2. Declare severity and owner; communicate a known status and update cadence.
3. Use logs, metrics, traces, and audit records to diagnose.
4. Mitigate, verify recovery, and monitor for recurrence.
5. Write a blameless review with contributing conditions and owned actions.

Use `core/docs/architecture/failure-and-chaos.md` as supporting reference for failure scenarios and experiments.
