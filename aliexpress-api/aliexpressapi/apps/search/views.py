# # Serializers
# from apps.products.serializers import ProductSerializer
# # Models
# from apps.products.models import Products

# # from django.contrib.auth import get_user_model
# from django.db.models import Q
# from drf_spectacular.utils import extend_schema
# from components.paginations.infinite_scroll import InfiniteScrollPagination
# from components.caching.search_cache import SearchCache
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
# from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

# search_cache = SearchCache()


# class SearchProductsViewSet(ViewSet):
#     """
#     Search products with pagination and caching.
#     """

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="q",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Search term for product name or description",
#                 required=True,
#             ),
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional) only for infinite scroll",
#                 required=False,
#             ),
#         ],
#         responses={200: ProductSerializer(many=True)},
#         tags=["Products Search"],
#         summary="Search All Products",
#         description="Search products by name or description with infinite scroll and cached results.",
#     )
#     def list(self, request):
#         try:
#             query = request.GET.get("q", "").strip().lower()
#             if not query:
#                 return Response(
#                     {"detail": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
#                 )

#             cursor = request.GET.get("cursor", "")

#             # Try to get cached response
#             cached_data = search_cache.get_results(query, cursor)
#             if cached_data:
#                 return Response(cached_data, status=status.HTTP_200_OK)

#             # Not cached - query DB
#             queryset = Products.objects.filter(
#                 Q(title__icontains=query) | Q(description__icontains=query)
#             ).order_by("-created_at")

#             paginator = InfiniteScrollPagination()
#             page_qs = paginator.paginate_queryset(queryset, request)

#             serializer = ProductSerializer(
#                 page_qs, many=True, context={"request": request}
#             )

#             response = paginator.get_paginated_response(serializer.data)

#             # Cache the response data for this query+cursor
#             search_cache.cache_results(query, response.data, cursor)

#             return response

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Serializers
from apps.products.serializers import ProductSerializer

# Models
from apps.products.models import Products

# Django ORM tools
from django.db.models import Q

# API Documentation helpers (drf-spectacular)
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# Custom components
from components.paginations.infinite_scroll import InfiniteScrollPagination
from components.caching.search_cache import SearchCache

# DRF core imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Instantiate search cache (could be backed by Redis, DB, or in-memory)
search_cache = SearchCache()


class SearchProductsViewSet(ViewSet):
    """
    ViewSet to search products by title or description.
    - Supports infinite scroll pagination.
    - Utilizes caching to reduce database load on repeated searches.
    """

    @extend_schema(
        parameters=[
            # Required query parameter for the search term
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search term for product name or description",
                required=True,
            ),
            # Optional cursor parameter for infinite scroll pagination
            OpenApiParameter(
                name="cursor",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Cursor for pagination (optional) only for infinite scroll",
                required=False,
            ),
        ],
        responses={200: ProductSerializer(many=True)},
        tags=["Products Search"],
        summary="Search All Products",
        description=(
            "Search products by name or description with infinite scroll "
            "pagination and cached results for performance."
        ),
    )
    def list(self, request):
        """
        Handles GET requests to search products.
        - Retrieves results from cache if available.
        - Falls back to querying the database.
        - Returns paginated results.
        """
        try:
            # 1️⃣ Extract and normalize the search query
            query = request.GET.get("q", "").strip().lower()
            if not query:
                # Return early if no search term provided
                return Response(
                    {"detail": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
                )

            # 2️⃣ Get pagination cursor (used for infinite scroll)
            cursor = request.GET.get("cursor", "")

            # 3️⃣ Check cache first (avoid hitting DB unnecessarily)
            cached_data = search_cache.get_results(query, cursor)
            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            # 4️⃣ If cache miss → Query database
            # Q objects allow OR conditions: title or description match
            queryset = Products.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-created_at")  # Newest products first

            # 5️⃣ Apply infinite scroll pagination
            paginator = InfiniteScrollPagination()
            page_qs = paginator.paginate_queryset(queryset, request)

            # 6️⃣ Serialize paginated queryset
            serializer = ProductSerializer(
                page_qs,
                many=True,
                context={"request": request},  # Context for absolute URLs
            )

            # 7️⃣ Generate paginated API response
            response = paginator.get_paginated_response(serializer.data)

            # 8️⃣ Store paginated result in cache (query + cursor specific)
            search_cache.cache_results(query, response.data, cursor)

            return response

        except Exception as e:
            # Catch unexpected errors to avoid breaking API contract
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
