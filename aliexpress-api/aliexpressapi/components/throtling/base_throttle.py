from typing import Optional, Tuple
from django.conf import settings
from rest_framework.throttling import BaseThrottle
from rest_framework.request import Request
from rest_framework.views import APIView

from .backend import CacheTokenBucket
from .exceptions import ThrottledError
from .utils import parse_rate


def throttling_rates():
    # Configure in settings.THROTTLING_RATES
    return getattr(
        settings,
        "THROTTLING_RATES",
        {
            "burst": "60/second",
            "sustained": "3000/min",
            "user": "600/min",
            "anon": "120/min",
        },
    )


class BaseScopedThrottle(BaseThrottle):
    """
    Production throttle based on a cache-backed token bucket.
    - Per-user when authenticated, otherwise per-IP.
    - Supports per-view 'throttle_scope' or class 'rate_name'.
    - Adds meta so middleware can publish X-RateLimit-* headers.
    """

    scope = None
    rate_name = None
    cost = 1
    ttl_seconds = 3600
    prefix = "throttle"

    def get_ident(self, request: Request) -> str:
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            return f"user:{user.pk}"
        # Fall back to IP
        ip = request.META.get("REMOTE_ADDR") or request._request.META.get("REMOTE_ADDR")
        return f"ip:{ip or 'unknown'}"

    def get_rate_str(self, request: Request, view: APIView) -> str:
        rates = throttling_rates()
        key = getattr(view, "throttle_scope", None) or self.scope or self.rate_name
        if key and key in rates:
            return rates[key]
        # fallback
        return rates.get("sustained", "3000/min")

    def get_bucket_key(self, request: Request, view: APIView) -> str:
        ident = self.get_ident(request)
        scope = (
            getattr(view, "throttle_scope", None)
            or self.scope
            or self.rate_name
            or "default"
        )
        method = request.method.upper()
        return f"{scope}:{method}:{ident}"

    def allow_request(self, request: Request, view: APIView) -> bool:
        rate = self.get_rate_str(request, view)
        capacity, refill = parse_rate(rate)
        bucket = CacheTokenBucket(
            prefix=self.prefix,
            capacity=capacity,
            refill_per_sec=refill,
            ttl_seconds=self.ttl_seconds,
        )
        key = self.get_bucket_key(request, view)
        result = bucket.allow(key, cost=self.cost)

        # stash for middleware/exception
        request._throttle_meta = {
            "allowed": result.allowed,
            "remaining": result.remaining,
            "reset_after": result.reset_after,
            "capacity": result.capacity,
            "rate": rate,
            "key": key,
        }
        return result.allowed

    def wait(self) -> Optional[float]:
        # DRF calls this but we raise our own exception with precise wait in throttled()
        return 1.0

    def throttled(self, request: Request, wait: Optional[float] = None):
        meta = getattr(request, "_throttle_meta", {}) or {}
        raise ThrottledError(
            wait=meta.get("reset_after", wait),
            meta={
                "remaining": meta.get("remaining"),
                "capacity": meta.get("capacity"),
                "rate": meta.get("rate"),
                "key": meta.get("key"),
            },
        )


class ScopedBurstThrottle(BaseScopedThrottle):
    rate_name = "burst"


class ScopedSustainedThrottle(BaseScopedThrottle):
    rate_name = "sustained"


class ScopedUserThrottle(BaseScopedThrottle):
    rate_name = "user"


class ScopedAnonThrottle(BaseScopedThrottle):
    rate_name = "anon"
