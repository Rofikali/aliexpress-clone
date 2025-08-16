from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if response.status_code == 429:
        # Ensure Retry-After header is set (DRF sets when Throttled(wait=...))
        if "Retry-After" not in response:
            wait = getattr(exc, "wait", None)
            if wait:
                response["Retry-After"] = str(int(wait))

        # Normalize payload
        detail = response.data.get("detail", "Request was throttled.")
        meta = getattr(exc, "meta", None) or {}
        response.data = {
            "error": "too_many_requests",
            "message": detail,
            "retry_after": int(getattr(exc, "wait", 1) or 1),
            "meta": meta,
        }
    return response
