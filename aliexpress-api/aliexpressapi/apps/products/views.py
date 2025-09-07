# new here
# apps.products/viewsets.py
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
from rest_framework.permissions import AllowAny

from components.paginations.base_pagination import BaseCursorPagination
from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import (
    # cache_factory,
    get_cache,
)  # ✅ generic cache factory


# apps.products/viewsets.py

# apps.products/viewsets.py


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
        description="Retrieve all products with cursor pagination and caching.",
    )
    def list(self, request):
        try:
            cursor = request.query_params.get("cursor") or "first"

            # ✅ Try cache first
            cache_data = self.cache.get_results(cursor)
            if cache_data:
                return ResponseFactory.success_collection(
                    items=cache_data.get("products", []),
                    pagination=cache_data.get("pagination", {}),
                    message="Products fetched successfully (cache)",
                    status=status.HTTP_200_OK,
                    request=request,
                    cache="HIT",
                )

            # ✅ DB + pagination
            queryset = Product.objects.all().order_by("-created_at")
            paginator = BaseCursorPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = ProductSerializer(
                page, many=True, context={"request": request}
            )

            response_data = paginator.get_paginated_response_data(serializer.data)

            # cache it
            self.cache.cache_results(cursor, response_data)

            return ResponseFactory.success_collection(
                items=response_data["items"],
                pagination=response_data["pagination"],
                message="Products fetched successfully",
                status=status.HTTP_200_OK,
                request=request,
            )

        except Exception as e:
            return ResponseFactory.error(
                message="Failed to fetch products",
                errors=[{"code": "SERVER_ERROR", "message": str(e)}],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                request=request,
            )

    @extend_schema(
        responses={200: ProductSerializer},
        tags=["Products"],
        summary="Retrieve Product",
        description="Retrieve a single Product by ID.",
    )
    def retrieve(self, request, pk=None):
        try:
            product = get_object_or_404(Product, id=pk)
            serializer = ProductSerializer(product, context={"request": request})
            return ResponseFactory.success_resource(
                item=serializer.data,
                message="Single Product fetched successfully",
                status=status.HTTP_200_OK,
                request=request,
            )
        except Exception as e:
            return ResponseFactory.error(
                message="Product not found",
                errors=[{"code": "NOT_FOUND", "message": str(e)}],
                status=status.HTTP_404_NOT_FOUND,
                request=request,
            )


# -------------------- PRODUCTS --------------------
# class ProductsViewSet(ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("products")

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

#             # ✅ Try cache
#             cache_data = self.cache.get_results(cursor)

#             if cache_data:
#                 return ResponseFactory.success(
#                     data=cache_data,
#                     message="Products fetched successfully",
#                     status=status.HTTP_200_OK,
#                     request=request,
#                     meta={"cursor": cursor},
#                     # extra={"cursor": cursor},
#                     cache="HIT",  # ✅ only pass when cached
#                 )

#             # ✅ DB + pagination
#             queryset = Product.objects.all().order_by("-created_at")
#             paginator = BaseCursorPagination()
#             paginator_queryset = paginator.paginate_queryset(queryset, request)

#             serializer = ProductSerializer(
#                 paginator_queryset, many=True, context={"request": request}
#             )
#             response_data = paginator.get_paginated_response(
#                 serializer.data
#             ).data  ### old one is curect
#             # response_data = paginator.get_paginated_response(serializer.data).data[
#             #     "products"
#             # ]

#             self.cache.cache_results(cursor, response_data)

#             # later for DB fetch
#             return ResponseFactory.success(
#                 data=response_data,
#                 message="Products fetched successfully",
#                 status=status.HTTP_200_OK,
#                 request=request,
#             )

#         except Exception as e:
#             return ResponseFactory.error(
#                 message="Failed to fetch products",
#                 errors={"detail": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 request=request,
#             )

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
#             serializer = ProductSerializer(product, context={"request": request})
#             return ResponseFactory.success(
#                 data=serializer.data,
#                 message="Single Product fetched successfully",
#                 status=status.HTTP_200_OK,
#                 request=request,
#             )
#         except Exception as e:
#             return ResponseFactory.error(
#                 message="Product not found",
#                 errors={"detail": str(e)},
#                 status=status.HTTP_404_NOT_FOUND,
#                 request=request,
#             )


# -------------------- CATEGORY --------------------
class CategoryViewSet(ViewSet):
    cache = get_cache("categories")

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="All Categories retrieve",
        description="Retrieve all product categories with caching.",
    )
    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="All Categories retrieve",
        description="Retrieve all product categories with caching.",
    )
    def list(self, request):
        cursor = "all"  # not paginated, static key
        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success(
                data=cache_data,
                message="Categories fetched successfully",
                request=request,
                extra={"from_cache": True},
                status=status.HTTP_200_OK,
            )

        queryset = Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(queryset, many=True)
        response_data = serializer.data

        self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success(
            data=response_data,
            message="Categories fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: CategorySerializer},
        tags=["Categories"],
        summary="Single Category retrieve",
        description="Retrieve a single category by ID.",
    )
    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return ResponseFactory.success(data=serializer.data, request=request)


# -------------------- BRAND --------------------
class BrandViewSet(ViewSet):
    cache = get_cache("brands")

    @extend_schema(
        responses={200: BrandSerializer(many=True)},
        tags=["Brands"],
        summary="All Brands retrieve",
        description="Retrieve all brands with caching.",
    )
    def list(self, request):
        cursor = "all"  # not paginated
        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success(
                data=cache_data,
                message="Brands fetched successfully",
                request=request,
                extra={"from_cache": True},
                status=status.HTTP_200_OK,
            )

        queryset = Brand.objects.all().order_by("-created_at")
        serializer = BrandSerializer(queryset, many=True)
        response_data = serializer.data

        self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success(
            data=response_data,
            message="Brands fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: BrandSerializer},
        tags=["Brands"],
        summary="Single Brand retrieve",
        description="Retrieve a single brand by ID.",
    )
    def retrieve(self, request, pk=None):
        brand = get_object_or_404(Brand, id=pk)
        serializer = BrandSerializer(brand)
        return ResponseFactory.success(data=serializer.data, request=request)


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

    @extend_schema(
        responses={200: ProductImageSerializer},
        tags=["Product Images"],
    )
    def retrieve(self, request, pk=None):
        image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- VARIANTS --------------------
class ProductVariantViewSet(ViewSet):
    @extend_schema(
        responses={200: ProductVariantSerializer(many=True)},
        tags=["Product Variants"],
    )
    def list(self, request):
        queryset = ProductVariant.objects.all()
        serializer = ProductVariantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: ProductVariantSerializer},
        tags=["Product Variants"],
    )
    def retrieve(self, request, pk=None):
        variant = get_object_or_404(ProductVariant, id=pk)
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- ATTRIBUTES --------------------
class ProductAttributeViewSet(ViewSet):
    @extend_schema(
        responses={200: ProductAttributeSerializer(many=True)},
        tags=["Product Attributes"],
    )
    def list(self, request):
        queryset = ProductAttribute.objects.all()
        serializer = ProductAttributeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: ProductAttributeSerializer},
        tags=["Product Attributes"],
    )
    def retrieve(self, request, pk=None):
        attr = get_object_or_404(ProductAttribute, id=pk)
        serializer = ProductAttributeSerializer(attr)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- INVENTORY --------------------
class InventoryViewSet(ViewSet):
    @extend_schema(
        responses={200: InventorySerializer(many=True)},
        tags=["Inventory"],
    )
    def list(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: InventorySerializer},
        tags=["Inventory"],
    )
    def retrieve(self, request, pk=None):
        stock = get_object_or_404(Inventory, id=pk)
        serializer = InventorySerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
