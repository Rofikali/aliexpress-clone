# components/pagination/base_cursor.py
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs


class BaseCursorPagination(CursorPagination):
    """
    Base cursor pagination class with:
    - Cleaner API response (returns only the cursor token, not full URL).
    - Configurable page size with an enforced max limit.
    - Consistent ordering (default: newest items first).

    Why use CursorPagination over OffsetPagination:
    - Prevents duplicate/missing records when new data is inserted during pagination.
    - More efficient on large datasets (avoids OFFSET/LIMIT on big tables).
    """

    # Default items per page if client doesn't provide ?page_size=
    page_size = 10

    # Allow clients to customize page size via query string (e.g., ?page_size=12)
    page_size_query_param = "page_size"

    # Upper bound for page size to prevent abuse (huge queries)
    max_page_size = 15

    # Default ordering — "newest first" by created_at
    # NOTE: Always ensure this matches your DB indexes for performance
    ordering = "-created_at"

    # Query parameter used by the frontend to pass the cursor token
    cursor_query_param = "cursor"

    def get_paginated_response(self, data):
        """
        Override DRF's default response to return:
        {
            "products": [...],   # serialized results
            "next_cursor": "...", # opaque token for next page or null
            "has_next": true/false
        }

        Why not return full URLs?
        - Clients (mobile/web) only need the token, not the full API URL.
        - Keeps payload smaller and frontend-agnostic.
        """
        return Response(
            {
                "products": data,
                "next_cursor": self.get_next_link_cursor(),
                "has_next": self.get_next_link() is not None,
            }
        )

    def get_next_link_cursor(self):
        """
        Extracts only the `cursor` token from DRF's generated next link.
        Example:
            DRF builds: https://api.example.com/products?cursor=abc123
            This method returns: "abc123"
        """
        next_link = self.get_next_link()
        if not next_link:
            return None

        # Parse query parameters from the URL
        params = parse_qs(urlparse(next_link).query)

        # Return first cursor value if present
        cursor = params.get(self.cursor_query_param)
        return cursor[0] if cursor else None
