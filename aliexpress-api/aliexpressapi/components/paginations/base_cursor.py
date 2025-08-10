# from rest_framework.response import Response
# from rest_framework.pagination import CursorPagination


# class CustomCursorPagination(CursorPagination):
#     # page_size = 10
#     ordering = "-created_at"  # Change to your model's date field

#     page_size = 10  # Default number of items per page
#     page_query_param = "page"  # Query parameter for the page number
#     page_size_query_param = "page_size"  # Allows clients to control the page size
#     max_page_size = 15  # Set an upper limit for page size to prevent abuse

#     def get_paginated_response(self, data):
#         return Response(
#             {
#                 "next": self.get_next_link(),  # URL for the next page
#                 "previous": self.get_previous_link(),  # URL for the previous page
#                 "page_size": len(data),  # Number of items in the current page
#                 "has_next": self.get_next_link()
#                 is not None,  # True if there is a next page
#                 # True if there is a previous page
#                 "has_previous": self.get_previous_link() is not None,
#                 "products": data,  # The paginated data
#             }
#         )


# components/pagination/base_cursor.py
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class BaseCursorPagination(CursorPagination):
    """
    Cursor pagination that returns a clean 'next_cursor' token and supports a
    page_size query param (with a max limit).
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 15
    ordering = "-created_at"  # default ordering, change per-view as needed
    cursor_query_param = "cursor"  # client passes ?cursor=...

    def get_paginated_response(self, data):
        """
        Provide a small, predictable response structure:
        {
          "results": [...],
          "next_cursor": "<cursor-token>" or null,
          "has_next": true/false
        }
        """
        return Response(
            {
                "products": data,
                "next_cursor": self.get_next_link_cursor(),
                "has_next": self.cursor is not None
                and self.get_next_link() is not None,
            }
        )

    def get_next_link_cursor(self):
        """
        Extract just the cursor token (not the full URL) for the next page.
        DRF builds full URLs; we want a small token clients can pass back.
        """
        next_link = self.get_next_link()
        if not next_link:
            return None
        # next_link looks like: ...?cursor=<token>
        from urllib.parse import urlparse, parse_qs

        qs = urlparse(next_link).query
        params = parse_qs(qs)
        cursor = params.get(self.cursor_query_param)
        return cursor[0] if cursor else None
