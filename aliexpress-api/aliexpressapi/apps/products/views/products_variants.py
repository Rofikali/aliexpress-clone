# # # # # new here
# # # # # apps.products/viewsets.py
# # # # from rest_framework.viewsets import ViewSet
# # # # from rest_framework.response import Response
# # # # from rest_framework import status
# # # # from django.shortcuts import get_object_or_404

# # # # from drf_spectacular.utils import extend_schema

# # # # from apps.products.models import (
# # # #     ProductVariant,
# # # # )
# # # # from apps.products.serializers.product_variants_serializer import (
# # # #     ProductVariantSerializer,
# # # # )


# # # # # -------------------- VARIANTS --------------------
# # # # class ProductVariantViewSet(ViewSet):
# # # #     @extend_schema(
# # # #         responses={200: ProductVariantSerializer(many=True)},
# # # #         tags=["Product Variants"],
# # # #     )
# # # #     def list(self, request):
# # # #         queryset = ProductVariant.objects.all()
# # # #         serializer = ProductVariantSerializer(queryset, many=True)
# # # #         return Response(serializer.data, status=status.HTTP_200_OK)

# # # #     @extend_schema(
# # # #         responses={200: ProductVariantSerializer},
# # # #         tags=["Product Variants"],
# # # #     )
# # # #     def retrieve(self, request, pk=None):
# # # #         variant = get_object_or_404(ProductVariant, id=pk)
# # # #         serializer = ProductVariantSerializer(variant)
# # # #         return Response(serializer.data, status=status.HTTP_200_OK)

# # # # apps/products/viewsets/product_variants_viewset.py
# # # from rest_framework.viewsets import ViewSet
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from django.shortcuts import get_object_or_404

# # # from drf_spectacular.utils import extend_schema

# # # from apps.products.models.product_variant_model import ProductVariant
# # # from apps.products.serializers.product_variants_serializer import (
# # #     ProductVariantSerializer,
# # # )


# # # class ProductVariantViewSet(ViewSet):
# # #     # route_name = "product-variants"  # will map to /products/:id/variants

# # #     def get_queryset(self, product_id=None):
# # #         qs = ProductVariant.objects.all()
# # #         if product_id:
# # #             qs = qs.filter(product_id=product_id)
# # #         return qs

# # #     @extend_schema(
# # #         responses={200: ProductVariantSerializer(many=True)},
# # #         tags=["Product Variants"],
# # #         summary="List product variants",
# # #     )
# # #     def list(self, request, product_pk=None):
# # #         queryset = self.get_queryset(product_pk)
# # #         serializer = ProductVariantSerializer(queryset, many=True)
# # #         return Response(serializer.data, status=status.HTTP_200_OK)

# # #     @extend_schema(
# # #         responses={200: ProductVariantSerializer},
# # #         tags=["Product Variants"],
# # #         summary="Retrieve single product variant",
# # #     )
# # #     def retrieve(self, request, pk=None, product_pk=None):
# # #         variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
# # #         serializer = ProductVariantSerializer(variant)
# # #         return Response(serializer.data, status=status.HTTP_200_OK)


# # # apps/products/views/product_variants_viewset.py
# # from rest_framework.viewsets import ViewSet
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.shortcuts import get_object_or_404
# # from drf_spectacular.utils import extend_schema

# # from apps.products.models.product_variant_model import ProductVariant
# # from apps.products.serializers.product_variants_serializer import ProductVariantSerializer


# # class ProductVariantViewSet(ViewSet):
# #     def get_queryset(self, product_id=None):
# #         qs = ProductVariant.objects.all()
# #         if product_id:
# #             qs = qs.filter(product_id=product_id)
# #         return qs

# #     @extend_schema(
# #         responses={200: ProductVariantSerializer(many=True)},
# #         tags=["Product Variants"],
# #         summary="List product variants",
# #     )
# #     def list(self, request, product_pk=None):
# #         queryset = self.get_queryset(product_pk)
# #         serializer = ProductVariantSerializer(queryset, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #     @extend_schema(
# #         responses={200: ProductVariantSerializer},
# #         tags=["Product Variants"],
# #         summary="Retrieve single product variant",
# #     )
# #     def retrieve(self, request, pk=None, product_pk=None):
# #         variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
# #         serializer = ProductVariantSerializer(variant)
# #         return Response(serializer.data, status=status.HTTP_200_OK)


# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from drf_spectacular.utils import extend_schema
# from components.responses.response_factory import ResponseFactory
# from apps.products.models.product_variant import ProductVariant
# from apps.products.serializers.product_variants import (
#     ProductVariantSerializer,
# )


# class ProductVariantViewSet(ViewSet):
#     def get_queryset(self, product_id=None):
#         qs = ProductVariant.objects.all()
#         if product_id:
#             qs = qs.filter(product_id=product_id)
#         return qs

#     @extend_schema(
#         responses={200: ProductVariantSerializer(many=True)},
#         tags=["Product Variants"],
#         summary="List product variants",
#     )
#     def list(self, request, product_pk=None):
#         queryset = self.get_queryset(product_pk)
#         serializer = ProductVariantSerializer(queryset, many=True)
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product variants retrieved successfully.",
#             status=status.HTTP_200_OK,
#         )

#     @extend_schema(
#         responses={200: ProductVariantSerializer},
#         tags=["Product Variants"],
#         summary="Retrieve single product variant",
#     )
#     def retrieve(self, request, pk=None, product_pk=None):
#         variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
#         serializer = ProductVariantSerializer(variant)
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product variant retrieved successfully.",
#             status=status.HTTP_200_OK,
#         )

# apps/products/views/product_variant_viewset.py
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q
from drf_spectacular.utils import extend_schema
from components.responses.response_factory import ResponseFactory
from components.paginations.base_pagination import BaseCursorPagination
from components.caching.cache_factory import get_cache

from apps.products.models.product_variant import ProductVariant, ProductVariantValue
from apps.products.serializers.product_variants import ProductVariantSerializer

# create cache instance (your custom cache class)
cache = get_cache("product_variants")


class ProductVariantViewSet(ViewSet):
    """
    Production-ready read-only endpoints for product variants.
    - list: supports cursor pagination (BaseCursorPagination) and simple attribute filters
    - retrieve: optimized with select_related + prefetch_related
    """

    @extend_schema(
        responses={200: ProductVariantSerializer(many=True)},
        tags=["Product Variants"],
        summary="List product variants",
    )
    def list(self, request, product_pk=None):
        # cursor handling for cache keys (same pattern as your products list)
        cursor = request.query_params.get("cursor") or "first"
        # page_size = request.query_params.get("page_size")

        # try cache first (your cache class exposes get_results / cache_results previously)
        # cache_data = cache.get_results(
        #     cursor, product_pk=product_pk, page_size=page_size
        # )
        # if cache_data:
        #     return ResponseFactory.success_collection(
        #         items=cache_data.get("items", []),
        #         pagination=cache_data.get("pagination", {}),
        #         message="Product variants fetched (cache)",
        #         status=status.HTTP_200_OK,
        #         request=request,
        #         cache="HIT",
        #     )

        cursor = request.query_params.get("cursor") or "first"
        cache_key = f"variants:{product_pk}:{cursor}"

        cache_data = cache.get_results(cache_key)
        if cache_data:
            return ResponseFactory.success_collection(
                items=cache_data.get("items", []),
                pagination=cache_data.get("pagination", {}),
                message="Product variants fetched (cache)",
                status=status.HTTP_200_OK,
                request=request,
                cache="HIT",
            )

        # base queryset: scope to product, only active variants (recommended)
        qs = ProductVariant.objects.filter(
            product_id=product_pk, is_active=True
        ).select_related("product")

        # allow simple attribute filtering: ?color=red&size=m (attribute names case-insensitive)
        # For each query param, match ProductVariantValue via related_name `varints` (or `values`)
        # We'll build Q objects for each param
        filter_q = Q()
        for k, v in request.query_params.items():
            # skip pagination params
            if k in ("cursor", "page_size"):
                continue
            # match attribute name -> value
            # note: this will generate joins; with proper indexes it's fine
            filter_q &= Q(
                **{f"varints__attribute__name__iexact": k, f"varints__value__iexact": v}
            )

        if filter_q:
            qs = qs.filter(filter_q).distinct()

        # prefetch variant values and attribute to avoid N+1
        qs = qs.prefetch_related(
            Prefetch(
                "varints",
                queryset=ProductVariantValue.objects.select_related("attribute"),
            )
        )

        # paginate with your BaseCursorPagination pattern
        paginator = BaseCursorPagination()
        page = paginator.paginate_queryset(qs.order_by("id"), request)
        serializer = ProductVariantSerializer(
            page, many=True, context={"request": request}
        )
        response_data = paginator.get_paginated_response_data(serializer.data)

        # cache the page results using your cache wrapper
        cache.cache_results(cursor, response_data, product_pk=product_pk)

        return ResponseFactory.success_collection(
            items=response_data["items"],
            pagination=response_data["pagination"],
            message="Product variants fetched",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        responses={200: ProductVariantSerializer},
        tags=["Product Variants"],
        summary="Retrieve single product variant",
    )
    def retrieve(self, request, pk=None, product_pk=None):
        # optimized queryset
        qs = ProductVariant.objects.select_related("product").filter(
            product_id=product_pk
        )
        qs = qs.prefetch_related(
            Prefetch(
                "varints",
                queryset=ProductVariantValue.objects.select_related("attribute"),
            )
        )

        variant = get_object_or_404(qs, id=pk)

        serializer = ProductVariantSerializer(variant, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Product variant retrieved successfully.",
            status=status.HTTP_200_OK,
            request=request,
        )
