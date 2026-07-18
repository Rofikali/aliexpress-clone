# Observability

## Signals

The backend emits JSON logs to standard output. Every HTTP response carries an `X-Request-ID`; incoming valid request IDs are preserved, otherwise the API creates one. Logs include `request_id`, `trace_id`, event name, HTTP method, path, status, and duration.

Prometheus metrics are exposed at `/metrics/`:

- `http_requests_total` by method, path, and status code.
- `http_request_duration_seconds` by method and path.
- `outbox_events` by delivery status.

In production, `/metrics/` requires `Authorization: Bearer <METRICS_BEARER_TOKEN>`. Restrict network access to the monitoring system as well; a bearer token is not a substitute for network policy.

## Outbox Delivery

The outbox worker claims events with a lease, then RabbitMQ publishes persistent, publisher-confirmed AMQP messages to the `marketplace.events` topic exchange. The message ID is the outbox event ID. Delivery is at-least-once, so every consumer must deduplicate by that ID.

Monitor pending-event age, processing-lease age, retry count, terminal failures, RabbitMQ queue depth, unacknowledged messages, and consumer lag. Page only when there is an owner and a defined action.

## Initial Alerts

1. API 5xx rate or p95 latency breaches its measured baseline.
2. `outbox_events{status="FAILED"}` is non-zero.
3. Pending or processing events exceed the worker lease/SLO window.
4. RabbitMQ queue depth grows while consumer throughput is zero.

## Trace Evolution

The current `trace_id` is log correlation. Add OpenTelemetry SDK/exporters only when a collector and an operational trace backend are selected; do not emit unusable spans without sampling, retention, and incident workflows.
