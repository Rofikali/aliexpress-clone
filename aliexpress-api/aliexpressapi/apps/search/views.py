# apps.search.views.py

# Serializers
from apps.products.serializers import ProductSerializer

# Models
from apps.products.models import Product

# Django ORM tools
from django.db.models import Q

# API Documentation helpers (drf-spectacular)
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# Custom components
# from components.paginations.infinite_scroll import InfiniteScrollPagination
from components.paginations.base_pagination import BaseCursorPagination

# from components.responses.response_factory import ResponseFactory
# from components.responses.error import ErrorResponse
from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import get_cache

# DRF core imports
from rest_framework import status
from rest_framework.viewsets import ViewSet


# ✅ Get cache via factory (instead of hardcoding SearchCache)
search_cache = get_cache("search")


class SearchProductsViewSet(ViewSet):
    """
    ViewSet to search products by title or description.
    - Supports infinite scroll pagination.
    - Utilizes caching to reduce database load on repeated searches.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search term for product name or description",
                required=True,
            ),
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
                return ResponseFactory.error(
                    message="No query provided.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    request=request,
                )

            # 2️⃣ Get pagination cursor (used for infinite scroll)
            cursor = request.GET.get("cursor", "")

            # 3️⃣ Check cache first
            cached_data = search_cache.get_results(query, cursor)
            if cached_data:
                return ResponseFactory.success(
                    body=cached_data,
                    message="Cached Products searched successfully",
                    status_code=status.HTTP_200_OK,
                    request=request,
                    extra={"cache_status": "HIT", "cursor": cursor},
                )

            # 4️⃣ DB query on cache miss
            queryset = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-created_at")

            # 5️⃣ Paginate
            paginator = BaseCursorPagination()
            page_qs = paginator.paginate_queryset(queryset, request)

            # 6️⃣ Serialize
            serializer = ProductSerializer(
                page_qs, many=True, context={"request": request}
            )

            # 7️⃣ Generate paginated response
            response = paginator.get_paginated_response(serializer.data)

            # 8️⃣ Store in cache
            search_cache.cache_results(query, response.data, cursor)

            return ResponseFactory.success(
                body=response.data,
                message="Products searched successfully",
                request=request,
                extra={"cache_status": "MISS", "cursor": cursor},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return ResponseFactory.error(
                message="Failed to search any products",
                errors={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                request=request,
            )
