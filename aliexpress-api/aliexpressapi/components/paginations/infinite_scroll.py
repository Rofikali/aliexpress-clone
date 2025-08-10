# from rest_framework.pagination import PageNumberPagination


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = "page_size"
#     max_page_size = 100


# apps/common/pagination/infinite_scroll.py
from .base_cursor import BaseCursorPagination


class InfiniteScrollPagination(BaseCursorPagination):
    """
    Use this in endpoints intended for infinite scroll. Keep page_size small,
    ordering should be stable (created_at + PK fallback if needed).
    """

    page_size = 10
    max_page_size = 15
    ordering = "-created_at"
