import time
from django.core.cache import cache


class RateLimitResult:
    __slots__ = ("allowed", "remaining", "reset_after", "capacity")

    def __init__(
        self, allowed: bool, remaining: int, reset_after: float, capacity: int
    ):
        self.allowed = allowed
        self.remaining = remaining
        self.reset_after = reset_after
        self.capacity = capacity


class CacheTokenBucket:
    """
    Token-bucket using Django cache. Works across instances IF your cache is shared
    (e.g., Memcached). It's not strictly atomic under heavy contention, but it’s
    robust and fast for most production APIs.
    Keys:
        <prefix>:<key>:tokens
        <prefix>:<key>:ts
    """

    def __init__(
        self, prefix: str, capacity: int, refill_per_sec: float, ttl_seconds: int = 3600
    ):
        self.prefix = prefix
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.ttl = ttl_seconds

    def _keys(self, key: str):
        base = f"{self.prefix}:{key}"
        return f"{base}:tokens", f"{base}:ts"

    def allow(self, key: str, cost: int = 1) -> RateLimitResult:
        tokens_key, ts_key = self._keys(key)
        now = time.time()

        # Fetch
        tokens = cache.get(tokens_key)
        ts = cache.get(ts_key)

        # Initialize on miss
        if tokens is None:
            tokens = float(self.capacity)
        else:
            tokens = float(tokens)

        if ts is None:
            ts = now
        else:
            ts = float(ts)

        # Refill
        delta = max(0.0, now - ts)
        filled = min(self.capacity, tokens + delta * self.refill_per_sec)

        # Consume
        if filled >= cost:
            remaining = filled - cost
            allowed = True
        else:
            remaining = filled
            allowed = False

        # Store
        cache.set(tokens_key, remaining, self.ttl)
        cache.set(ts_key, now, self.ttl)

        needed = max(0.0, cost - filled)
        reset_after = (needed / self.refill_per_sec) if needed > 0 else 0.0

        return RateLimitResult(allowed, int(remaining), reset_after, int(self.capacity))
