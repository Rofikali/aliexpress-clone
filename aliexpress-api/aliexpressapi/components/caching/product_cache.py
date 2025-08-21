# # components/caching/product_cache.py
# import hashlib
# from components.caching.base_cache import BaseCache


# class ProductCache(BaseCache):
#     """
#     File-based product-listing cache. Keys are MD5 hashed to be filesystem-safe.
#     """

#     def __init__(self):
#         super().__init__("product", default_ttl=600)  # 10 minutes

#     def _hash_key(self, raw: str) -> str:
#         return hashlib.md5(raw.encode()).hexdigest()

#     def make_key(self, cursor: str = "", extra: str = "") -> str:
#         """
#         Build a stable key for a listing page. `extra` can include filters/sort.
#         """
#         raw = f"product:{cursor}:{extra}"
#         return self._hash_key(raw)

#     def cache_results(self, cursor: str, data):
#         key = self.make_key(cursor)
#         self.set(key, data)

#     def get_results(self, cursor: str):
#         key = self.make_key(cursor)
#         return self.get(key)


# components/caching/product_cache.py

import hashlib
from components.caching.base_cache import BaseCache
from components.utils.encoders import dumps, loads  # ✅ import our custom encoder


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
        """
        Save results in cache with safe JSON encoding.
        """
        key = self.make_key(cursor)
        serialized_data = dumps(data)  # ✅ Use custom encoder
        self.set(key, serialized_data)

    def get_results(self, cursor: str):
        """
        Retrieve results from cache and decode JSON.
        """
        key = self.make_key(cursor)
        serialized_data = self.get(key)
        if serialized_data:
            return loads(serialized_data)  # ✅ Deserialize JSON
        return None
