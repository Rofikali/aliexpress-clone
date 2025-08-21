# from rest_framework.viewsets import ViewSet
# from .models import Product
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ProductSerializer
# from django.shortcuts import get_object_or_404

# ## for API Docs
# from drf_spectacular.utils import extend_schema

# # paginations are here
# from components.paginations.infinite_scroll import InfiniteScrollPagination

# """
# # Cache for search results

# # class productsViewSet(ViewSet):
# #     @extend_schema(
# #         request=ProductSerializer,
# #         responses={200: ProductSerializer},
# #         tags=["Products"],
# #         summary="All Products retrieve",
# #         description="This endpoint allows you to retrieve a All Product.",
# #     )
# #     def list(self, request):
# #         queryset = Products.objects.all()
# #         paginator = InfiniteScrollPagination()
# #         paginator_queryset = paginator.paginate_queryset(queryset, request)
# #         serializer = ProductSerializer(
# #             paginator_queryset, many=True, context={"request": request}
# #         )
# #         return paginator.get_paginated_response(serializer.data)

# """
# from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
# from components.caching.product_cache import ProductCache


# class ProductsViewSet(ViewSet):
#     product_cache = ProductCache()  # Cache instance

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional). Leave empty or 'first' to fetch first page.",
#                 required=False,
#             ),
#         ],
#         request=ProductSerializer,
#         responses={200: ProductSerializer(many=True)},
#         tags=["Products"],
#         summary="All Products retrieve",
#         description="This endpoint allows you to retrieve all products, supports pagination with cursor.",
#     )
#     def list(self, request):
#         try:
#             cursor = (
#                 request.query_params.get("cursor") or "first"
#             )  # Use 'first' for initial cache key

#             # Try cache first
#             cache_data = self.product_cache.get_results(cursor)
#             if cache_data:
#                 return Response(cache_data, status=status.HTTP_200_OK)

#             # Cache miss: query DB and paginate
#             queryset = Product.objects.all().order_by("-created_at")
#             paginator = InfiniteScrollPagination()
#             paginator_queryset = paginator.paginate_queryset(queryset, request)

#             serializer = ProductSerializer(
#                 paginator_queryset, many=True, context={"request": request}
#             )
#             response_data = paginator.get_paginated_response(serializer.data).data

#             # Cache the serialized response data with cursor as key
#             self.product_cache.cache_results(cursor, response_data)

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": f"An unexpected error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# # Product DetailViewSet here
# class ProductViewSet(ViewSet):
#     @extend_schema(
#         request=ProductSerializer,
#         responses={200: ProductSerializer},
#         tags=["Products"],
#         summary="Single Product retrieve",
#         description="This endpoint allows you to retrieve a single Product.",
#     )
#     def retrieve(self, request, pk=None):
#         try:
#             product = get_object_or_404(Product, id=pk)
#             product_serializer = ProductSerializer(
#                 product, context={"request": request}
#             )
#             return Response(
#                 {"product": product_serializer.data},
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# new here
# products/api/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    ProductAttribute,
    Inventory,
)
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductVariantSerializer,
    ProductAttributeSerializer,
    InventorySerializer,
)

from components.paginations.infinite_scroll import InfiniteScrollPagination
from components.caching.product_cache import ProductCache  # ✅ your cache


# -------------------- PRODUCTS --------------------
# class ProductsViewSet(ViewSet):
#     product_cache = ProductCache()

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional). Leave empty or 'first' to fetch first page.",
#                 required=False,
#             ),
#         ],
#         request=ProductSerializer,
#         responses={200: ProductSerializer(many=True)},
#         tags=["Products"],
#         summary="All Products retrieve",
#         description="Retrieve all products with cursor pagination and caching.",
#     )
#     def list(self, request):
#         try:
#             cursor = request.query_params.get("cursor") or "first"

#             # Try cache
#             cache_data = self.product_cache.get_results(cursor)
#             if cache_data:
#                 return Response(cache_data, status=status.HTTP_200_OK)

#             # DB + pagination
#             queryset = Product.objects.all().order_by("-created_at")
#             paginator = InfiniteScrollPagination()
#             paginator_queryset = paginator.paginate_queryset(queryset, request)

#             serializer = ProductSerializer(
#                 paginator_queryset, many=True, context={"request": request}
#             )
#             response_data = paginator.get_paginated_response(serializer.data).data

#             # Cache result
#             self.product_cache.cache_results(cursor, response_data)

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class ProductViewSet(ViewSet):
#     @extend_schema(
#         request=ProductSerializer,
#         responses={200: ProductSerializer},
#         tags=["Products"],
#         summary="Single Product retrieve",
#         description="Retrieve a single Product by ID.",
#     )
#     def retrieve(self, request, pk=None):
#         try:
#             product = get_object_or_404(Product, id=pk)
#             product_serializer = ProductSerializer(
#                 product, context={"request": request}
#             )
#             return Response(
#                 {"product": product_serializer.data}, status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from components.responses.success import SuccessResponse
from components.responses.error import ErrorResponse


# -------------------- PRODUCTS --------------------
class ProductsViewSet(ViewSet):
    product_cache = ProductCache()

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
        description="Retrieve all products with cursor pagination and caching.",
    )
    def list(self, request):
        try:
            cursor = request.query_params.get("cursor") or "first"

            # Try cache
            cache_data = self.product_cache.get_results(cursor)
            if cache_data:
                return SuccessResponse.send(
                    data=cache_data,
                    message="Products fetched successfully",
                    request=request,
                    extra={"cursor": cursor, "from_cache": True},  # HIT auto
                    code=status.HTTP_200_OK,
                )

            # DB + pagination (MISS)
            queryset = Product.objects.all().order_by("-created_at")
            paginator = InfiniteScrollPagination()
            paginator_queryset = paginator.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                paginator_queryset, many=True, context={"request": request}
            )
            response_data = paginator.get_paginated_response(serializer.data).data

            # Cache result
            self.product_cache.cache_results(cursor, response_data)

            return SuccessResponse.send(
                data=response_data,
                message="Products fetched successfully",
                request=request,
                extra={"cursor": cursor},  # MISS by default
                code=status.HTTP_200_OK,
            )

        except Exception as e:
            return ErrorResponse.send(
                message="Failed to fetch products",
                errors={"detail": str(e)},
                request=request,
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -------------------- SINGLE PRODUCT --------------------
class ProductViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
        tags=["Products"],
        summary="Single Product retrieve",
        description="Retrieve a single Product by ID.",
    )
    def retrieve(self, request, pk=None):
        try:
            product = get_object_or_404(Product, id=pk)
            serializer = ProductSerializer(product, context={"request": request})
            return SuccessResponse.send(data=serializer.data, request=request)
        except Exception as e:
            return ErrorResponse.send(
                message="Product not found", errors=str(e), request=request
            )


# -------------------- CATEGORY --------------------
class CategoryViewSet(ViewSet):
    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="All Categories retrieve",
        description="Retrieve all product categories.",
    )
    def list(self, request):
        queryset = Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: CategorySerializer},
        tags=["Categories"],
        summary="Single Category retrieve",
        description="Retrieve a single category by ID.",
    )
    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- BRAND --------------------
class BrandViewSet(ViewSet):
    @extend_schema(
        responses={200: BrandSerializer(many=True)},
        tags=["Brands"],
        summary="All Brands retrieve",
        description="Retrieve all brands.",
    )
    def list(self, request):
        queryset = Brand.objects.all().order_by("-created_at")
        serializer = BrandSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: BrandSerializer},
        tags=["Brands"],
        summary="Single Brand retrieve",
        description="Retrieve a single brand by ID.",
    )
    def retrieve(self, request, pk=None):
        brand = get_object_or_404(Brand, id=pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- PRODUCT IMAGES --------------------
class ProductImageViewSet(ViewSet):
    @extend_schema(
        responses={200: ProductImageSerializer(many=True)},
        tags=["Product Images"],
    )
    def list(self, request):
        queryset = ProductImage.objects.all()
        serializer = ProductImageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- VARIANTS --------------------
class ProductVariantViewSet(ViewSet):
    def list(self, request):
        queryset = ProductVariant.objects.all()
        serializer = ProductVariantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        variant = get_object_or_404(ProductVariant, id=pk)
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- ATTRIBUTES --------------------
class ProductAttributeViewSet(ViewSet):
    def list(self, request):
        queryset = ProductAttribute.objects.all()
        serializer = ProductAttributeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        attr = get_object_or_404(ProductAttribute, id=pk)
        serializer = ProductAttributeSerializer(attr)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- INVENTORY --------------------
class InventoryViewSet(ViewSet):
    def list(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        stock = get_object_or_404(Inventory, id=pk)
        serializer = InventorySerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
