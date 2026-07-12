# Backend Contracts and Evolution

## HTTP API

- Keep externally consumed endpoints under `/api/v1/`.
- Use DRF serializers as boundary DTOs, not as the business model.
- Publish the OpenAPI schema in CI and treat breaking changes as review-blocking.
- Standardize errors: `code`, `message`, `details`, `request_id`.
- Paginated responses and money values must have stable, documented formats.

## Events

Each integration event includes `event_id`, `event_type`, `version`, `occurred_at`, `correlation_id`, `aggregate_id`, and `payload`. Store an outbox row with the same database transaction as the state change. Consumers must deduplicate by `event_id` and be retry-safe.

Events announce facts (`order.placed.v1`); commands request work (`ReserveInventory`). Do not use events for synchronous validation required to return an HTTP response.

## Future Service Extraction

1. Prove the module boundary inside the monolith first.
2. Replace direct cross-module calls with a port and a contract test.
3. Publish/consume the outbox event internally.
4. Move the module's data ownership, worker, API adapter, and observability together.
5. Run both paths behind a feature flag, reconcile data, then retire the old path.

The database is not an integration API. A future service must not read another service's tables.

## Required Tests

- Unit tests for domain rules and use cases.
- Integration tests for Django repositories and database constraints.
- Contract tests for public API and events.
- End-to-end tests for checkout, payment webhook, cancellation, and refund journeys.
