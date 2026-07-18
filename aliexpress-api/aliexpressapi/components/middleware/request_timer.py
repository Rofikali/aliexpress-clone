import logging
import time
from uuid import UUID, uuid4

from components.observability.context import request_id, trace_id
from components.observability.metrics import HTTP_REQUEST_DURATION, HTTP_REQUESTS


logger = logging.getLogger(__name__)


class RequestTimerMiddleware:
    """
    Middleware to track request processing time (latency).
    Adds request.start_time so we can calculate latency in responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        request._start_time = time.time()
        request.request_id = self._request_id(request.headers.get("X-Request-ID"))
        request.trace_id = self._trace_id(request.headers.get("traceparent"))
        request_id_token = request_id.set(request.request_id)
        trace_id_token = trace_id.set(request.trace_id)

        try:
            response = self.get_response(request)
            response["X-Request-ID"] = request.request_id
            return response
        finally:
            duration = time.perf_counter() - started_at
            status_code = getattr(locals().get("response"), "status_code", 500)
            path = request.path_info
            resolver_match = getattr(request, "resolver_match", None)
            metric_path = getattr(resolver_match, "route", None) or "unmatched"
            HTTP_REQUESTS.labels(
                method=request.method,
                path=metric_path,
                status_code=status_code,
            ).inc()
            HTTP_REQUEST_DURATION.labels(method=request.method, path=metric_path).observe(
                duration
            )
            logger.info(
                "http_request_completed",
                extra={
                    "event": "http_request_completed",
                    "http_method": request.method,
                    "http_path": path,
                    "http_status_code": status_code,
                    "duration_ms": round(duration * 1000, 2),
                },
            )
            request_id.reset(request_id_token)
            trace_id.reset(trace_id_token)

    def _request_id(self, value):
        try:
            return str(UUID(value))
        except (TypeError, ValueError, AttributeError):
            return str(uuid4())

    def _trace_id(self, traceparent):
        if traceparent:
            parts = traceparent.split("-")
            if len(parts) == 4 and len(parts[1]) == 32:
                try:
                    int(parts[1], 16)
                    return parts[1]
                except ValueError:
                    pass
        return uuid4().hex
