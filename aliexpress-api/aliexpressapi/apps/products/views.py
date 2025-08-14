from rest_framework.viewsets import ViewSet
from .models import Products
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404

## for API Docs
from drf_spectacular.utils import extend_schema

# paginations are here
from components.paginations.infinite_scroll import InfiniteScrollPagination

"""
# Cache for search results

# class productsViewSet(ViewSet):
#     @extend_schema(
#         request=ProductSerializer,
#         responses={200: ProductSerializer},
#         tags=["Products"],
#         summary="All Products retrieve",
#         description="This endpoint allows you to retrieve a All Product.",
#     )
#     def list(self, request):
#         queryset = Products.objects.all()
#         paginator = InfiniteScrollPagination()
#         paginator_queryset = paginator.paginate_queryset(queryset, request)
#         serializer = ProductSerializer(
#             paginator_queryset, many=True, context={"request": request}
#         )
#         return paginator.get_paginated_response(serializer.data)

"""
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from components.caching.product_cache import ProductCache


class ProductsViewSet(ViewSet):
    product_cache = ProductCache()  # Cache instance

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="cursor",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Cursor for pagination (optional). Leave empty or 'first' to fetch first page.",
                required=False,
            ),
        ],
        request=ProductSerializer,
        responses={200: ProductSerializer(many=True)},
        tags=["Products"],
        summary="All Products retrieve",
        description="This endpoint allows you to retrieve all products, supports pagination with cursor.",
    )
    def list(self, request):
        try:
            cursor = (
                request.query_params.get("cursor") or "first"
            )  # Use 'first' for initial cache key

            # Try cache first
            cache_data = self.product_cache.get_results(cursor)
            if cache_data:
                return Response(cache_data, status=status.HTTP_200_OK)

            # Cache miss: query DB and paginate
            queryset = Products.objects.all().order_by("-created_at")
            paginator = InfiniteScrollPagination()
            paginator_queryset = paginator.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                paginator_queryset, many=True, context={"request": request}
            )
            response_data = paginator.get_paginated_response(serializer.data).data

            # Cache the serialized response data with cursor as key
            self.product_cache.cache_results(cursor, response_data)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Product DetailViewSet here
class ProductViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
        tags=["Products"],
        summary="Single Product retrieve",
        description="This endpoint allows you to retrieve a single Product.",
    )
    def retrieve(self, request, pk=None):
        try:
            product = get_object_or_404(Products, id=pk)
            product_serializer = ProductSerializer(
                product, context={"request": request}
            )
            return Response(
                {"product": product_serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
