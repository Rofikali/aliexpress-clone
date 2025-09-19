# # # apps.products/views/product_view.py
# # from rest_framework.viewsets import ViewSet
# # from rest_framework import status
# # from django.shortcuts import get_object_or_404

# # from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# # from apps.products.models.product_model import (
# #     Product,
# # )
# # from apps.products.serializers.products_serializser import (
# #     ProductSerializer,
# #     ProductDetailSerializer,
# # )
# # from rest_framework.permissions import AllowAny

# # from components.paginations.base_pagination import BaseCursorPagination
# # from components.responses.response_factory import ResponseFactory
# # from components.caching.cache_factory import (
# #     # cache_factory,
# #     get_cache,
# # )  # ✅ generic cache factory


# # class ProductsViewSet(ViewSet):
# #     permission_classes = [AllowAny]
# #     cache = get_cache("products")

# #     @extend_schema(
# #         parameters=[
# #             OpenApiParameter(
# #                 name="cursor",
# #                 type=OpenApiTypes.STR,
# #                 location=OpenApiParameter.QUERY,
# #                 description="Cursor for pagination (optional). Use 'first' for initial page.",
# #                 required=False,
# #             ),
# #             OpenApiParameter(
# #                 name="page_size",
# #                 type=OpenApiTypes.INT,
# #                 location=OpenApiParameter.QUERY,
# #                 description="Number of items per page (default=12, max=50).",
# #                 required=False,
# #             ),
# #         ],
# #         responses={200: ProductSerializer(many=True)},
# #         tags=["Products"],
# #         summary="List Products",
# #         description="Retrieve all products with cursor pagination and caching.",
# #     )
# #     def list(self, request):
# #         try:
# #             cursor = request.query_params.get("cursor") or "first"

# #             # ✅ Try cache first
# #             cache_data = self.cache.get_results(cursor)
# #             if cache_data:
# #                 return ResponseFactory.success_collection(
# #                     items=cache_data.get("items", []),
# #                     pagination=cache_data.get("pagination", {}),
# #                     message="Products fetched successfully (cache)",
# #                     status=status.HTTP_200_OK,
# #                     request=request,
# #                     cache="HIT",
# #                 )

# #             # ✅ DB + pagination
# #             queryset = Product.objects.all().order_by("-created_at")
# #             paginator = BaseCursorPagination()
# #             page = paginator.paginate_queryset(queryset, request)
# #             serializer = ProductSerializer(
# #                 page, many=True, context={"request": request}
# #             )

# #             response_data = paginator.get_paginated_response_data(serializer.data)

# #             # cache it
# #             self.cache.cache_results(cursor, response_data)

# #             return ResponseFactory.success_collection(
# #                 items=response_data["items"],
# #                 pagination=response_data["pagination"],
# #                 message="Products fetched successfully",
# #                 status=status.HTTP_200_OK,
# #                 request=request,
# #             )

# #         except Exception as e:
# #             return ResponseFactory.error(
# #                 message="Failed to fetch products",
# #                 errors=[{"code": "SERVER_ERROR", "message": str(e)}],
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #                 request=request,
# #             )

# #     @extend_schema(
# #         responses={200: ProductSerializer},
# #         tags=["Products"],
# #         summary="Retrieve Product",
# #         description="Retrieve a single Product by ID.",
# #     )
# #     def retrieve(self, request, pk=None):
# #         try:
# #             product = get_object_or_404(Product, id=pk)
# #             serializer = ProductDetailSerializer(product, context={"request": request})
# #             return ResponseFactory.success_resource(
# #                 item=serializer.data,
# #                 message="Single Product fetched successfully",
# #                 status=status.HTTP_200_OK,
# #                 request=request,
# #             )
# #         except Exception as e:
# #             return ResponseFactory.error(
# #                 message="Product not found",
# #                 errors=[{"code": "NOT_FOUND", "message": str(e)}],
# #                 status=status.HTTP_404_NOT_FOUND,
# #                 request=request,
# #             )


# # apps/products/views/product_view.py
# from rest_framework.viewsets import ViewSet
# from rest_framework import status
# from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# from apps.products.models.product_model import Product
# from apps.products.serializers.products_serializser import (
#     ProductSerializer,
#     ProductDetailSerializer,
# )
# from rest_framework.permissions import AllowAny
# from components.paginations.base_pagination import BaseCursorPagination
# from components.responses.response_factory import ResponseFactory
# from components.caching.cache_factory import get_cache


# class ProductsViewSet(ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("products")

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional). Use 'first' for initial page.",
#                 required=False,
#             ),
#             OpenApiParameter(
#                 name="page_size",
#                 type=OpenApiTypes.INT,
#                 location=OpenApiParameter.QUERY,
#                 description="Number of items per page (default=12, max=50).",
#                 required=False,
#             ),
#         ],
#         responses={200: ProductSerializer(many=True)},
#         tags=["Products"],
#         summary="List Products",
#         description="Retrieve all products with cursor pagination and caching.",
#     )
#     def list(self, request):
#         cursor = request.query_params.get("cursor") or "first"

#         # Try cache
#         cache_data = self.cache.get_results(cursor)
#         if cache_data:
#             return ResponseFactory.success_collection(
#                 items=cache_data.get("items", []),
#                 pagination=cache_data.get("pagination", {}),
#                 message="Products fetched successfully (cache)",
#                 status=status.HTTP_200_OK,
#                 request=request,
#                 cache="HIT",
#             )

#         queryset = Product.objects.all().order_by("-created_at")
#         paginator = BaseCursorPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = ProductSerializer(page, many=True, context={"request": request})

#         response_data = paginator.get_paginated_response_data(serializer.data)
#         self.cache.cache_results(cursor, response_data)

#         return ResponseFactory.success_collection(
#             items=response_data["items"],
#             pagination=response_data["pagination"],
#             message="Products fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         responses={200: ProductDetailSerializer},
#         tags=["Products"],
#         summary="Retrieve Product",
#         description="Retrieve a single Product by ID.",
#     )
#     def retrieve(self, request, pk=None):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductDetailSerializer(product, context={"request": request})
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Single Product fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )


from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.permissions import AllowAny

from apps.products.models.product_model import Product
from apps.products.serializers.products_serializser import (
    ProductSerializer,
    ProductDetailSerializer,
)
from components.paginations.base_pagination import BaseCursorPagination
from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import get_cache


class ProductsViewSet(ViewSet):
    permission_classes = [AllowAny]
    cache = get_cache("products")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="cursor",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Cursor for pagination (optional). Use 'first' for initial page.",
                required=False,
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Number of items per page (default=12, max=50).",
                required=False,
            ),
        ],
        responses={200: ProductSerializer(many=True)},
        tags=["Products"],
        summary="List Products",
    )
    def list(self, request):
        cursor = request.query_params.get("cursor") or "first"

        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success_collection(
                items=cache_data.get("items", []),
                pagination=cache_data.get("pagination", {}),
                message="Products fetched successfully (cache)",
                status=status.HTTP_200_OK,
                request=request,
                cache="HIT",
            )

        queryset = Product.objects.all().order_by("-created_at")
        paginator = BaseCursorPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(page, many=True, context={"request": request})

        response_data = paginator.get_paginated_response_data(serializer.data)
        self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success_collection(
            items=response_data["items"],
            pagination=response_data["pagination"],
            message="Products fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        responses={200: ProductDetailSerializer},
        tags=["Products"],
        summary="Retrieve Product",
    )
    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductDetailSerializer(product, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Single Product fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )
