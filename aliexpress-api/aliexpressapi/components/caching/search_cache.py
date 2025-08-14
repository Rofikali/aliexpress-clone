import hashlib
from components.caching.base_cache import BaseCache


class SearchCache(BaseCache):
    def __init__(self):
        super().__init__("search", default_ttl=120)  # 2 min cache

    def _hash_key(self, raw: str) -> str:
        return hashlib.md5(raw.encode()).hexdigest()

    def make_key(self, query: str, cursor: str = "") -> str:
        raw = f"search:{query}:{cursor or 'first'}"
        return self._hash_key(raw)

    def cache_results(self, query: str, results: list, cursor: str = ""):
        key = self.make_key(query, cursor)
        self.set(key, results)

    def get_results(self, query: str, cursor: str = ""):
        key = self.make_key(query, cursor)
        return self.get(key)
