# # # cache/base_cache.py
# # import json
# # import time
# # from pathlib import Path

# # CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "file_cache"
# # # print('cache_dir is ', CACHE_DIR)
# # CACHE_DIR.mkdir(exist_ok=True)


# # class BaseCache:
# #     def __init__(self, namespace: str, default_ttl: int = 300):
# #         """
# #         namespace: separate folder for each cache type (e.g. 'product', 'search')
# #         default_ttl: cache expiration time in seconds
# #         """
# #         self.namespace = namespace
# #         self.default_ttl = default_ttl
# #         self.cache_path = CACHE_DIR / namespace
# #         self.cache_path.mkdir(exist_ok=True)

# #     def _get_file_path(self, key: str) -> Path:
# #         """Returns the file path for the cache key."""
# #         safe_key = key.replace("/", "_")  # avoid subfolder issues
# #         return self.cache_path / f"{safe_key}.json"

# #     def set(self, key: str, value, ttl: int = None):
# #         """Save value to cache with optional custom TTL."""
# #         expire_time = int(time.time()) + (ttl or self.default_ttl)
# #         data = {"expire": expire_time, "value": value}
# #         with open(self._get_file_path(key), "w", encoding="utf-8") as f:
# #             json.dump(data, f)

# #     def get(self, key: str):
# #         """Get cached value if not expired, else return None."""
# #         file_path = self._get_file_path(key)
# #         if not file_path.exists():
# #             return None
# #         try:
# #             with open(file_path, "r", encoding="utf-8") as f:
# #                 data = json.load(f)
# #             if data["expire"] >= int(time.time()):
# #                 return data["value"]
# #             else:
# #                 file_path.unlink(missing_ok=True)  # remove expired file
# #         except (json.JSONDecodeError, KeyError):
# #             file_path.unlink(missing_ok=True)  # remove corrupted file
# #         return None

# #     def delete(self, key: str):
# #         """Delete specific cache key."""
# #         file_path = self._get_file_path(key)
# #         file_path.unlink(missing_ok=True)

# #     def clear(self):
# #         """Clear all cache for this namespace."""
# #         for file in self.cache_path.glob("*.json"):
# #             file.unlink(missing_ok=True)

# components/caching/base_cache.py

import time
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAIN_CACHE_DIR = BASE_DIR / "file_cache"


@contextmanager
def atomic_write(path: Path, mode="wb"):
    """
    Context manager for atomic file writes.
    Ensures partial writes don't corrupt cache.
    """
    temp = path.with_suffix(".tmp")
    try:
        with open(temp, mode) as f:
            yield f
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


class BaseCache:
    """
    Base file cache class handling folder structure,
    TTL expiration, atomic writes, and clearing namespace.
    """

    def __init__(self, namespace: str, default_ttl: int = 600):
        self.namespace = namespace
        self.default_ttl = default_ttl
        self._ensure_dirs()

    def _ensure_dirs(self):
        """
        Auto-create main file_cache and namespace folders.
        """
        MAIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        (MAIN_CACHE_DIR / self.namespace).mkdir(parents=True, exist_ok=True)
        self.cache_dir = MAIN_CACHE_DIR / self.namespace

    def _file_path(self, key: str) -> Path:
        self._ensure_dirs()
        safe_key = key.replace("/", "_")  # safe filename
        return self.cache_dir / f"{safe_key}.cache"

    def _is_expired(self, file_path: Path) -> bool:
        if not file_path.exists():
            return True
        age = time.time() - file_path.stat().st_mtime
        return age > self.default_ttl

    def get(self, key: str):
        self._ensure_dirs()
        file_path = self._file_path(key)
        if self._is_expired(file_path):
            if file_path.exists():
                file_path.unlink()
            return None
        try:
            with open(file_path, "rb") as f:
                return f.read().decode("utf-8")
        except Exception:
            return None

    def set(self, key: str, data: str, ttl: int = None):
        self._ensure_dirs()
        file_path = self._file_path(key)
        try:
            with atomic_write(file_path) as f:
                f.write(data.encode("utf-8"))
        except Exception:
            pass

    def clear(self):
        """
        Clear all cache files in this namespace.
        """
        self._ensure_dirs()
        for file in self.cache_dir.glob("*.cache"):
            try:
                file.unlink()
            except:
                pass
