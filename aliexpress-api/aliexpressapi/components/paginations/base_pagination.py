# components/pagination/base_pagination.py
from rest_framework.pagination import CursorPagination
from urllib.parse import urlparse, parse_qs


class BaseCursorPagination(CursorPagination):
    """
    Standardized cursor pagination.

    ✅ Clean API response:
       - Returns only cursor tokens, not full URLs
       - Always returns pagination info inside `meta`
    ✅ Safer for huge datasets (cursor-based, avoids OFFSET/LIMIT problems)
    ✅ Matches GitHub/Stripe-style APIs
    """

    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50
    ordering = "-created_at"
    cursor_query_param = "cursor"

    def get_paginated_response_data(self, data: list) -> dict:
        """
        Returns only the raw pagination payload (no Response object).
        Used by ResponseFactory.
        """
        return {
            "items": data,
            "pagination": {
                "next_cursor": self.get_next_link_cursor(),
                "has_next": self.get_next_link() is not None,
                # "count": len(data),
            },
        }

    def get_next_link_cursor(self):
        """
        Extracts only the opaque `cursor` token from DRF's next link.
        Example:
            Input: https://api.example.com/products?cursor=abc123
            Output: "abc123"
        """
        next_link = self.get_next_link()
        if not next_link:
            return None

        params = parse_qs(urlparse(next_link).query)
        cursor = params.get(self.cursor_query_param)
        return cursor[0] if cursor else None
