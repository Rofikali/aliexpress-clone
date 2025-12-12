# # apps/products/views/product_attribute_viewset.py
# from rest_framework import viewsets, status
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import AllowAny

# from apps.products.models.product_attribute import ProductAttribute

# # from apps.products.serializers.products_serializser import ProductAttributeSerializer
# from apps.products.serializers.product_attribute import (
#     ProductAttributeSerializer,
# )


# from components.responses.response_factory import ResponseFactory


# from components.paginations.base_pagination import BaseCursorPagination
# from components.caching.cache_factory import get_cache


# class ProductAttributeViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("product_attributes")

#     def get_queryset(self):
#         """Return attributes strictly linked to this variant via ProductVariantValue."""
#         variant_id = self.kwargs.get("variant_pk")
#         print(f"[DEBUG:get_queryset] variant_pk = {variant_id}")
#         qs = (
#             ProductAttribute.objects.filter(productvariantvalue__variant_id=variant_id)
#             .distinct()
#             .order_by("sort_order")
#         )
#         print(f"[DEBUG:get_queryset] SQL = {str(qs.query)}")
#         return qs

#     path_parameters = [
#         OpenApiParameter(
#             name="product_pk",
#             type=OpenApiTypes.UUID,
#             location=OpenApiParameter.PATH,
#             description="UUID of the parent Product",
#         ),
#         OpenApiParameter(
#             name="variant_pk",
#             type=OpenApiTypes.UUID,
#             location=OpenApiParameter.PATH,
#             description="UUID of the parent Product Variant",
#         ),
#     ]

#     @extend_schema(
#         parameters=path_parameters,
#         responses={200: ProductAttributeSerializer(many=True)},
#         tags=["Product Attributes"],
#         summary="List all attributes for a product variant",
#     )
#     def list(self, request, product_pk=None, variant_pk=None):
#         print(f"[DEBUG:list] product_pk={product_pk}, variant_pk={variant_pk}")

#         cursor = request.query_params.get("cursor") or "first"
#         cache_key = f"{variant_pk}:{cursor}"
#         print(f"[DEBUG:list] cache_key={cache_key}")

#         cache_data = self.cache.get_results(cache_key)
#         if cache_data:
#             print("[DEBUG:list] Cache HIT")
#             return ResponseFactory.success_collection(
#                 items=cache_data.get("items", []),
#                 pagination=cache_data.get("pagination", {}),
#                 message="Product attributes fetched successfully (cache)",
#                 status=status.HTTP_200_OK,
#                 request=request,
#                 cache="HIT",
#             )

#         print("[DEBUG:list] Cache MISS, hitting DB...")
#         queryset = self.get_queryset()
#         paginator = BaseCursorPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = ProductAttributeSerializer(
#             page, many=True, context={"request": request}
#         )
#         response_data = paginator.get_paginated_response_data(serializer.data)

#         print(f"[DEBUG:list] items_count={len(response_data['items'])}")
#         self.cache.cache_results(cache_key, response_data)

#         return ResponseFactory.success_collection(
#             items=response_data["items"],
#             pagination=response_data["pagination"],
#             message="Product attributes fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         responses={200: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#     )
#     def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
#         print(
#             f"[DEBUG:retrieve] product_pk={product_pk}, variant_pk={variant_pk}, pk={pk}"
#         )

#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         print(f"[DEBUG:retrieve] Found attribute -> {attribute}")

#         serializer = ProductAttributeSerializer(attribute, context={"request": request})
#         print(f"[DEBUG:retrieve] Serialized data -> {serializer.data}")

#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

