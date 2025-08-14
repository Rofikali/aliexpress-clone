# components/caching/product_cache.py
import hashlib
from components.caching.base_cache import BaseCache


class ProductCache(BaseCache):
    """
    File-based product-listing cache. Keys are MD5 hashed to be filesystem-safe.
    """

    def __init__(self):
        super().__init__("product", default_ttl=600)  # 10 minutes

    def _hash_key(self, raw: str) -> str:
        return hashlib.md5(raw.encode()).hexdigest()

    def make_key(self, cursor: str = "", extra: str = "") -> str:
        """
        Build a stable key for a listing page. `extra` can include filters/sort.
        """
        raw = f"product:{cursor}:{extra}"
        return self._hash_key(raw)

    def cache_results(self, cursor: str, data):
        key = self.make_key(cursor)
        self.set(key, data)

    def get_results(self, cursor: str):
        key = self.make_key(cursor)
        return self.get(key)
