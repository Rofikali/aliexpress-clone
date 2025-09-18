import hashlib
from components.caching.base_cache import BaseCache
from components.utils.encoders import dumps, loads


class CacheFactory(BaseCache):
    """
    Generic file-based cache for any namespace (product, category, brand, etc).
    Uses MD5 hashed keys to keep them filesystem-safe.
    """

    def __init__(self, namespace: str, default_ttl: int = 600):
        super().__init__(namespace, default_ttl=default_ttl)

    def _hash_key(self, raw: str) -> str:
        return hashlib.md5(raw.encode()).hexdigest()

    def make_key(self, cursor: str = "", extra: str = "") -> str:
        raw = f"{self.namespace}:{cursor}:{extra}"
        return self._hash_key(raw)

    def cache_results(self, cursor: str, data, extra: str = ""):
        key = self.make_key(cursor, extra)
        serialized_data = dumps(data)
        self.set(key, serialized_data)

    def get_results(self, cursor: str, extra: str = ""):
        key = self.make_key(cursor, extra)
        serialized_data = self.get(key)
        if serialized_data:
            return loads(serialized_data)
        return None


# ---------------------------
# 🔹 Cache Registry
# ---------------------------

CACHE_REGISTRY = {}


def get_cache(namespace: str, ttl: int = 600) -> CacheFactory:
    """
    Get or create a cache for a given namespace.
    Example: get_cache("product"), get_cache("category")
    """
    if namespace not in CACHE_REGISTRY:
        CACHE_REGISTRY[namespace] = CacheFactory(namespace, default_ttl=ttl)
    return CACHE_REGISTRY[namespace]
