# apps/common/pagination/infinite_scroll.py
from .base_cursor import BaseCursorPagination


class InfiniteScrollPagination(BaseCursorPagination):
    """
    Specialized cursor pagination for infinite scroll UI patterns.

    Key differences from BaseCursorPagination:
    - Fixed small page size for smooth UX (default: 10 items per request).
    - Ordering is strictly descending by creation date (newest first).
    - Works best with stable ordering fields + index for performance.

    ⚠️ Production note:
    - When using cursor pagination with descending ordering, new items
      inserted at the top will not appear in already-fetched pages.
      This is expected behavior and preferable for infinite scroll UX.
    """

    # Keep page size small for faster response & better scroll experience
    page_size = 12
    max_page_size = 15

    # Ensure ordering is stable (created_at DESC)
    # Optional: Add secondary ordering by PK for tie-breakers in DB
    ordering = "-created_at"
