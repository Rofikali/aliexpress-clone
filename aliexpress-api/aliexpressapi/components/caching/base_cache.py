# cache/base_cache.py
import json
import time
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "file_cache"
# print('cache_dir is ', CACHE_DIR)
CACHE_DIR.mkdir(exist_ok=True)


class BaseCache:
    def __init__(self, namespace: str, default_ttl: int = 300):
        """
        namespace: separate folder for each cache type (e.g. 'product', 'search')
        default_ttl: cache expiration time in seconds
        """
        self.namespace = namespace
        self.default_ttl = default_ttl
        self.cache_path = CACHE_DIR / namespace
        self.cache_path.mkdir(exist_ok=True)

    def _get_file_path(self, key: str) -> Path:
        """Returns the file path for the cache key."""
        safe_key = key.replace("/", "_")  # avoid subfolder issues
        return self.cache_path / f"{safe_key}.json"

    def set(self, key: str, value, ttl: int = None):
        """Save value to cache with optional custom TTL."""
        expire_time = int(time.time()) + (ttl or self.default_ttl)
        data = {"expire": expire_time, "value": value}
        with open(self._get_file_path(key), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def get(self, key: str):
        """Get cached value if not expired, else return None."""
        file_path = self._get_file_path(key)
        if not file_path.exists():
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data["expire"] >= int(time.time()):
                return data["value"]
            else:
                file_path.unlink(missing_ok=True)  # remove expired file
        except (json.JSONDecodeError, KeyError):
            file_path.unlink(missing_ok=True)  # remove corrupted file
        return None

    def delete(self, key: str):
        """Delete specific cache key."""
        file_path = self._get_file_path(key)
        file_path.unlink(missing_ok=True)

    def clear(self):
        """Clear all cache for this namespace."""
        for file in self.cache_path.glob("*.json"):
            file.unlink(missing_ok=True)
