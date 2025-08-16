from django.utils.deprecation import MiddlewareMixin


class RateLimitHeadersMiddleware(MiddlewareMixin):
    """
    Publishes standard X-RateLimit-* headers when throttle meta is present.
    Add after authentication middleware so request.user is available.
    """

    def process_response(self, request, response):
        meta = getattr(request, "_throttle_meta", None)
        if meta:
            capacity = meta.get("capacity")
            remaining = meta.get("remaining")
            reset_after = meta.get("reset_after")

            # These header names are conventional; tweak if you prefer RFC headers
            response["X-RateLimit-Limit"] = (
                str(capacity) if capacity is not None else ""
            )
            response["X-RateLimit-Remaining"] = (
                str(remaining) if remaining is not None else ""
            )
            response["X-RateLimit-Reset"] = (
                f"{reset_after:.3f}" if reset_after is not None else ""
            )

            # For 429, DRF sets Retry-After via exception wait; but ensure it’s present if meta is here
            if response.status_code == 429 and reset_after is not None:
                response["Retry-After"] = str(int(max(1, reset_after)))
        return response
