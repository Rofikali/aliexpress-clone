# from rest_framework.viewsets import ViewSet
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
# from rest_framework.permissions import AllowAny

# from apps.products.models.product import Product
# from apps.products.serializers.product import (
#     ProductSerializer,
#     ProductDetailSerializer,
# )
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
#     )
#     def list(self, request):
#         cursor = request.query_params.get("cursor") or "first"

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
#     )
#     # def retrieve(self, request, pk=None):
#     #     product = get_object_or_404(Product, id=pk)
#     #     #  add here filters that returns only related products
#     #     serializer = ProductDetailSerializer(product, context={"request": request})
#     #     return ResponseFactory.success_resource(
#     #         item=serializer.data,
#     #         message="Single Product fetched successfully",
#     #         status=status.HTTP_200_OK,
#     #         request=request,
#     #     )
#     def retrieve(self, request, pk=None):
#         product = get_object_or_404(
#             Product.objects.select_related("category", "brand").prefetch_related(
#                 "product_images"
#             ),
#             id=pk,
#         )

#         serializer = ProductDetailSerializer(product, context={"request": request})
#         data = serializer.data  # main product data

#         # ---- RELATED PRODUCTS LOGIC ----
#         related = Product.objects.filter(
#             category=product.category, is_active=True
#         ).exclude(id=product.id)[:12]

#         data["related_products"] = ProductSerializer(
#             related, many=True, context={"request": request}
#         ).data

#         # You can add more sections later:
#         # data["reviews"] = ...
#         # data["recommendations"] = ...
#         # data["similar_tags"] = ...
#         # etc

#         return ResponseFactory.success_resource(
#             item=data,
#             message="Single Product fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )


# apps/products/views/product_viewset.py
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.viewsets import ViewSet
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import get_cache
from components.paginations.base_pagination import BaseCursorPagination

from apps.products.models.product import Product
from apps.products.models.product_variant import ProductVariant, ProductVariantValue

# from apps.products.serializers.products_serializser import ProductDetailSerializer
from apps.products.serializers.product_variants import ProductVariantSerializer
from apps.products.services.variant_service import ProductVariantService
from apps.products.serializers.product import (
    ProductSerializer,
    ProductDetailSerializer,
)


class ProductsViewSet(ViewSet):
    permission_classes = []  # set your permissions
    pagination_class = BaseCursorPagination
    cache = get_cache("products")  # product-level cache
    # permission_classes = [AllowAny]
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
        parameters=[
            OpenApiParameter(
                name="include",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="optional: 'variants' to include variants payload",
            ),
        ],
        responses={200: ProductDetailSerializer},
        tags=["Products"],
        summary="Retrieve Product (optionally include variants)",
    )
    def retrieve(self, request, pk=None):
        include = request.query_params.get("include")
        cache_key = f"product:{pk}:include:{include or 'none'}"

        # try cache first
        cache_data = None
        try:
            cache_data = self.cache.get_results(cache_key)
        except TypeError:
            # fallback: your cache implementation might expect only cursor etc.
            cache_data = self.cache.get_results(cache_key)

        if cache_data:
            return ResponseFactory.success_resource(
                item=cache_data,
                message="Product (cache)",
                status=status.HTTP_200_OK,
                request=request,
                cache="HIT",
            )

        # load product
        product_qs = Product.objects.select_related("brand", "category")
        if include == "variants":
            product_qs = product_qs.prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.prefetch_related(
                        Prefetch(
                            "attributes",
                            queryset=ProductVariantValue.objects.select_related(
                                "attribute", "value"
                            ),
                        )
                    ),
                )
            )

        product = get_object_or_404(product_qs, id=pk)
        serializer = ProductDetailSerializer(product, context={"request": request})
        data = serializer.data

        # include variants payload if requested
        if include == "variants":
            # Use VariantService to build canonical payload (no pagination)
            # We reuse the same builder to ensure the same shape as /variants/ endpoint
            with ProductVariantService.fetch_variants(product_id=pk) as qs:
                variants = list(qs)  # all variants prefetched for product
            bundle = ProductVariantService.build_response_data(variants)

            data["variants"] = ProductVariantSerializer(
                variants, many=True, context={"request": request}
            ).data
            data["available_attributes"] = bundle.available_attributes
            data["combination_map"] = bundle.combination_map

        # cache and return
        try:
            self.cache.cache_results(cache_key, data)
        except Exception:
            # best-effort cache; don't break response if cache fails
            pass

        return ResponseFactory.success_resource(
            item=data,
            message="Product retrieved",
            status=status.HTTP_200_OK,
            request=request,
            cache="MISS",
        )
