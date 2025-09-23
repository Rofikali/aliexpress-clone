# # new here
# # apps.products/viewsets.py
# from rest_framework.viewsets import ViewSet
# from rest_framework import status
# from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema

# from apps.products.models.category import Category
# from apps.products.serializers.category import CategorySerializer

# from components.responses.response_factory import ResponseFactory
# from components.caching.cache_factory import (
#     # cache_factory,
#     get_cache,
# )  # ✅ generic cache factory


# # -------------------- CATEGORY --------------------
# class CategoryViewSet(ViewSet):
#     cache = get_cache("categories")

#     @extend_schema(
#         responses={200: CategorySerializer(many=True)},
#         tags=["Categories"],
#         summary="All Categories retrieve",
#         description="Retrieve all product categories with caching.",
#     )
#     @extend_schema(
#         responses={200: CategorySerializer(many=True)},
#         tags=["Categories"],
#         summary="All Categories retrieve",
#         description="Retrieve all product categories with caching.",
#     )
#     def list(self, request):
#         cursor = "all"  # not paginated, static key
#         cache_data = self.cache.get_results(cursor)
#         if cache_data:
#             return ResponseFactory.success_collection(
#                 items=cache_data,
#                 message="Categories fetched successfully",
#                 request=request,
#                 status=status.HTTP_200_OK,
#             )

#         queryset = Category.objects.all().order_by("-created_at")
#         serializer = CategorySerializer(queryset, many=True)
#         response_data = serializer.data

#         self.cache.cache_results(cursor, response_data)

#         return ResponseFactory.success(
#             data=response_data,
#             message="Categories fetched successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )

#     @extend_schema(
#         responses={200: CategorySerializer},
#         tags=["Categories"],
#         summary="Single Category retrieve",
#         description="Retrieve a single category by ID.",
#     )
#     def retrieve(self, request, pk=None):
#         category = get_object_or_404(Category, id=pk)
#         serializer = CategorySerializer(category)
#         return ResponseFactory.success(data=serializer.data, request=request)


# from rest_framework.viewsets import ViewSet
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from apps.products.models.category import Category
# from apps.products.serializers.category import CategorySerializer
# from apps.products.serializers.product import ProductSerializer
# # from apps.utils.response_factory import ResponseFactory
# from components.responses.response_factory import ResponseFactory

# from components.caching.cache_factory import get_cache
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# class CategoryViewSet(ViewSet):
#     cache = get_cache("categories")

#     def list(self, request):
#         """Return all categories"""
#         cache_data = self.cache.get_results("all")
#         if cache_data:
#             return ResponseFactory.success_collection(
#                 items=cache_data,
#                 message="Categories fetched successfully",
#                 request=request,
#                 status=status.HTTP_200_OK,
#             )

#         queryset = Category.objects.all().order_by("-created_at")
#         serializer = CategorySerializer(queryset, many=True)
#         response_data = serializer.data

#         self.cache.cache_results("all", response_data)

#         return ResponseFactory.success(
#             data=response_data,
#             message="Categories fetched successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )

#     def retrieve(self, request, pk=None):
#         """Return single category + all related products"""
#         category = get_object_or_404(Category, id=pk)

#         # Get all products for this category
#         products = category.product_set.all().order_by("-created_at")
#         products_serializer = ProductSerializer(
#             products, many=True, context={"request": request}
#         )

#         category_serializer = CategorySerializer(category)

#         data = category_serializer.data
#         data["products"] = products_serializer.data

#         return ResponseFactory.success(
#             data=data,
#             message="Category and related products fetched successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from apps.products.models.category import Category
from apps.products.serializers.category import CategorySerializer
from apps.products.serializers.product import ProductSerializer
from components.responses.response_factory import ResponseFactory
from apps.products.serializers.category_with_products import (
    CategoryWithProductsSerializer,
)
from components.caching.cache_factory import get_cache
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from components.paginations.base_pagination import BaseCursorPagination


class CategoryViewSet(ViewSet):
    cache = get_cache("categories")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="cursor",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Cursor for pagination (optional). Use 'all' for initial fetch.",
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
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="List all categories",
        description="Retrieve all product categories with optional caching.",
    )
    def list(self, request):
        """Return all categories"""
        queryset = Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(queryset, many=True)
        response_data = serializer.data

        return ResponseFactory.success_collection(
            items=response_data,
            message="Categories fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description="ID of the category",
                required=True,
            ),
        ],
        responses={200: "CategoryWithProductsSerializer"},
        tags=["Categories"],
        summary="Retrieve single category with products",
        description="Retrieve a single category by ID along with all related products.",
    )
    # def retrieve(self, request, pk=None):
    #     cursor = request.query_params.get("cursor") or "first"
    #     cache_data = self.cache.get_results(cursor)
    #     if cache_data:
    #         return ResponseFactory.success_collection(
    #             items=cache_data.get("items", []),
    #             pagination=cache_data.get("pagination", {}),
    #             message="Category Products fetched successfully (cache)",
    #             status=status.HTTP_200_OK,
    #             request=request,
    #             cache="HIT",
    #         )
    #     """Return single category + all related products"""
    #     category = get_object_or_404(Category, id=pk)
    #     paginator = BaseCursorPagination()
    #     page = paginator.paginate_queryset(category, request)
    #     serializer = CategoryWithProductsSerializer(
    #         page, category, context={"request": request}
    #     )
    #     response_data = paginator.get_paginated_response_data(serializer.data)
    #     self.cache.cache_results(cursor, response_data)

    #     return ResponseFactory.success_collection(
    #         items=response_data["items"],
    #         pagination=response_data["pagination"],
    #         message="Products fetched successfully",
    #         status=status.HTTP_200_OK,
    #         request=request,
    #     )

    #     # return ResponseFactory.success_collection(
    #     #     item=serializer.data,
    #     #     message="Category and related products fetched successfully",
    #     #     request=request,
    #     #     status=status.HTTP_200_OK,
    #     # )

    def retrieve(self, request, pk=None):
        cursor = request.query_params.get("cursor") or "first"

        # 🔹 1. Try cache
        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success_collection(
                items=cache_data.get("items", []),
                pagination=cache_data.get("pagination", {}),
                message="Category Products fetched successfully (cache)",
                status=status.HTTP_200_OK,
                request=request,
                cache="HIT",
            )

        # 🔹 2. Fetch category
        category = get_object_or_404(Category, id=pk)

        # 🔹 3. Paginate related products
        products_qs = category.category_products.all().order_by("-created_at")
        paginator = BaseCursorPagination()
        page = paginator.paginate_queryset(products_qs, request)

        # 🔹 4. Serialize
        products_serialzer = ProductSerializer(
            page, many=True, context={"request": request}
        )

        # 🔹 5. Pagination data
        response_data = paginator.get_paginated_response_data(products_serialzer.data)

        # 🔹 6. Cache results
        self.cache.cache_results(cursor, response_data)

        # 🔹 7. Response
        return ResponseFactory.success_collection(
            items=response_data["items"],  # wrap in list for consistency
            pagination=response_data["pagination"],
            message="Related Products fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )
