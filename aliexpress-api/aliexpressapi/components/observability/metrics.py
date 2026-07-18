from prometheus_client import Counter, Gauge, Histogram


HTTP_REQUESTS = Counter(
    "http_requests_total",
    "HTTP responses emitted by the API",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)
OUTBOX_EVENTS = Gauge(
    "outbox_events",
    "Outbox events by delivery state",
    ["status"],
)
