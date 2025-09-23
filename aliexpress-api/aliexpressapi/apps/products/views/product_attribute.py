# # from rest_framework import viewsets, status
# # from rest_framework.response import Response
# # from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# # from apps.products.models.product_attribute_model import ProductAttribute
# # from apps.products.serializers.product_attribute_serializer import (
# #     ProductAttributeSerializer,
# # )


# # class ProductAttributeViewSet(viewsets.ViewSet):
# #     """
# #     Manage product attributes nested under variants.
# #     """

# #     def get_queryset(self):
# #         variant_id = self.kwargs.get("variant_pk")
# #         return ProductAttribute.objects.filter(variant_id=variant_id)

# #     # Common parameters for all actions
# #     path_parameters = [
# #         OpenApiParameter(
# #             name="product_pk",
# #             type=OpenApiTypes.INT,
# #             location=OpenApiParameter.PATH,
# #             description="ID of the parent Product",
# #         ),
# #         OpenApiParameter(
# #             name="variant_pk",
# #             type=OpenApiTypes.INT,
# #             location=OpenApiParameter.PATH,
# #             description="ID of the parent Product Variant",
# #         ),
# #     ]

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={200: ProductAttributeSerializer(many=True)},
# #         tags=["Product Attributes"],
# #         summary="List all attributes for a product variant",
# #         description="Retrieve all attributes belonging to a specific product variant.",
# #     )
# #     def list(self, request, product_pk=None, variant_pk=None):
# #         queryset = self.get_queryset()
# #         serializer = ProductAttributeSerializer(queryset, many=True)
# #         return Response(serializer.data)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={200: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Retrieve a single attribute",
# #         description="Retrieve a single attribute by its ID for a given product variant.",
# #     )
# #     def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
# #         try:
# #             attribute = self.get_queryset().get(pk=pk)
# #         except ProductAttribute.DoesNotExist:
# #             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
# #         serializer = ProductAttributeSerializer(attribute)
# #         return Response(serializer.data)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         request=ProductAttributeSerializer,
# #         responses={201: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Create a new attribute",
# #         description="Create a new attribute for a specific product variant.",
# #     )
# #     def create(self, request, product_pk=None, variant_pk=None):
# #         data = request.data.copy()
# #         data["product"] = product_pk
# #         data["variant"] = variant_pk
# #         serializer = ProductAttributeSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         request=ProductAttributeSerializer,
# #         responses={200: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Update an attribute",
# #         description="Update an existing attribute (full or partial update).",
# #     )
# #     def update(self, request, pk=None, product_pk=None, variant_pk=None):
# #         try:
# #             attribute = self.get_queryset().get(pk=pk)
# #         except ProductAttribute.DoesNotExist:
# #             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

# #         serializer = ProductAttributeSerializer(
# #             attribute, data=request.data, partial=True
# #         )
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={204: None},
# #         tags=["Product Attributes"],
# #         summary="Delete an attribute",
# #         description="Delete an attribute by ID from a product variant.",
# #     )
# #     def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
# #         try:
# #             attribute = self.get_queryset().get(pk=pk)
# #         except ProductAttribute.DoesNotExist:
# #             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

# #         attribute.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)

# # # apps/products/views/product_attribute_viewset.py
# # from rest_framework import viewsets, status
# # from rest_framework.response import Response
# # from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
# # from django.shortcuts import get_object_or_404
# # from components.responses.response_factory import ResponseFactory
# # from components.paginations.base_pagination import BaseCursorPagination
# # from components.caching.cache_factory import get_cache
# # from apps.products.models.product_attribute_model import ProductAttribute
# # from apps.products.serializers.product_attribute_serializer import (
# #     ProductAttributeSerializer,
# # )
# # from rest_framework.permissions import AllowAny


# # class ProductAttributeViewSet(viewsets.ViewSet):
# #     permission_classes = [AllowAny]
# #     cache = get_cache("products")

# #     def get_queryset(self):
# #         variant_id = self.kwargs.get("variant_pk")
# #         return ProductAttribute.objects.filter(variant_id=variant_id)

# #     # common params for docs

# #     path_parameters = [
# #         OpenApiParameter(
# #             name="product_pk",
# #             type=OpenApiTypes.UUID,  # <-- fix here
# #             location=OpenApiParameter.PATH,
# #             description="UUID of the parent Product",
# #         ),
# #         OpenApiParameter(
# #             name="variant_pk",
# #             type=OpenApiTypes.UUID,  # <-- fix here
# #             location=OpenApiParameter.PATH,
# #             description="UUID of the parent Product Variant",
# #         ),
# #     ]

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={200: ProductAttributeSerializer(many=True)},
# #         tags=["Product Attributes"],
# #         summary="List all attributes for a product variant",
# #     )
# #     def list(self, request, product_pk=None, variant_pk=None):
# #         queryset = self.get_queryset()
# #         serializer = ProductAttributeSerializer(queryset, many=True)
# #         # return Response(serializer.data)
# #         return ResponseFactory.success_collection(
# #             items=serializer.data,
# #             message="Product attributes fetched successfully",
# #             pagination=None,
# #             status=status.HTTP_200_OK,
# #             request=request,
# #             # items=response_data["items"],
# #             # pagination=response_data["pagination"],
# #             # message="Products fetched successfully",
# #             # status=status.HTTP_200_OK,
# #             # request=request,
# #         )

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={200: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Retrieve a single attribute",
# #     )
# #     def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
# #         attribute = get_object_or_404(self.get_queryset(), pk=pk)
# #         serializer = ProductAttributeSerializer(attribute)
# #         return Response(serializer.data)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         request=ProductAttributeSerializer,
# #         responses={201: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Create a new attribute",
# #     )
# #     def create(self, request, product_pk=None, variant_pk=None):
# #         data = request.data.copy()
# #         data["product"] = product_pk
# #         data["variant"] = variant_pk
# #         serializer = ProductAttributeSerializer(data=data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         request=ProductAttributeSerializer,
# #         responses={200: ProductAttributeSerializer},
# #         tags=["Product Attributes"],
# #         summary="Update an attribute",
# #     )
# #     def update(self, request, pk=None, product_pk=None, variant_pk=None):
# #         attribute = get_object_or_404(self.get_queryset(), pk=pk)
# #         serializer = ProductAttributeSerializer(
# #             attribute, data=request.data, partial=True
# #         )
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         return Response(serializer.data)

# #     @extend_schema(
# #         parameters=path_parameters,
# #         responses={204: None},
# #         tags=["Product Attributes"],
# #         summary="Delete an attribute",
# #     )
# #     def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
# #         attribute = get_object_or_404(self.get_queryset(), pk=pk)
# #         attribute.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)


# # apps/products/views/product_attribute_viewset.py
# from rest_framework import viewsets, status
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import AllowAny

# from components.responses.response_factory import ResponseFactory
# from components.paginations.base_pagination import BaseCursorPagination
# from components.caching.cache_factory import get_cache

# from apps.products.models.product_attribute_model import ProductAttribute
# from apps.products.serializers.product_attribute_serializer import (
#     ProductAttributeSerializer,
# )


# class ProductAttributeViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("product_attributes")  # 🔥 cache namespace just for attributes

#     def get_queryset(self):
#         variant_id = self.kwargs.get("variant_pk")
#         return ProductAttribute.objects.filter(variant_id=variant_id).order_by(
#             "-created_at"
#         )

#     # shared docs params
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
#         parameters=path_parameters
#         + [
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
#         responses={200: ProductAttributeSerializer(many=True)},
#         tags=["Product Attributes"],
#         summary="List all attributes for a product variant",
#         description="Retrieve product variant attributes with cursor pagination and caching.",
#     )
#     def list(self, request, product_pk=None, variant_pk=None):
#         cursor = request.query_params.get("cursor") or "first"

#         # ✅ check cache first
#         cache_key = f"{variant_pk}:{cursor}"
#         cache_data = self.cache.get_results(cache_key)
#         if cache_data:
#             return ResponseFactory.success_collection(
#                 items=cache_data.get("items", []),
#                 pagination=cache_data.get("pagination", {}),
#                 message="Product attributes fetched successfully (cache)",
#                 status=status.HTTP_200_OK,
#                 request=request,
#                 cache="HIT",
#             )

#         queryset = self.get_queryset()
#         paginator = BaseCursorPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = ProductAttributeSerializer(
#             page, many=True, context={"request": request}
#         )

#         response_data = paginator.get_paginated_response_data(serializer.data)
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
#         summary="Retrieve a single attribute",
#     )
#     def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         serializer = ProductAttributeSerializer(attribute, context={"request": request})
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={201: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#         summary="Create a new attribute",
#     )
#     def create(self, request, product_pk=None, variant_pk=None):
#         data = request.data.copy()
#         data["variant"] = variant_pk  # only variant required now
#         serializer = ProductAttributeSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # 🔥 invalidate cache for this variant
#         self.cache.clear_prefix(variant_pk)

#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute created successfully",
#             status=status.HTTP_201_CREATED,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={200: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#         summary="Update an attribute",
#     )
#     def update(self, request, pk=None, product_pk=None, variant_pk=None):
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         serializer = ProductAttributeSerializer(
#             attribute, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # 🔥 clear cache
#         self.cache.clear_prefix(variant_pk)

#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute updated successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         responses={204: None},
#         tags=["Product Attributes"],
#         summary="Delete an attribute",
#     )
#     def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         attribute.delete()

#         # 🔥 clear cache
#         self.cache.clear_prefix(variant_pk)

#         return ResponseFactory.success_message(
#             message="Product attribute deleted successfully",
#             status=status.HTTP_204_NO_CONTENT,
#             request=request,
#         )

# apps/products/views/product_attribute_viewset.py
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from apps.products.models.product_attribute import ProductAttribute

# from apps.products.serializers.products_serializser import ProductAttributeSerializer
from apps.products.serializers.product_attribute import (
    ProductAttributeSerializer,
)


from components.responses.response_factory import ResponseFactory


from components.paginations.base_pagination import BaseCursorPagination
from components.caching.cache_factory import get_cache


class ProductAttributeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    cache = get_cache("product_attributes")

    def get_queryset(self):
        """Return attributes strictly linked to this variant via ProductVariantValue."""
        variant_id = self.kwargs.get("variant_pk")
        print(f"[DEBUG:get_queryset] variant_pk = {variant_id}")
        qs = (
            ProductAttribute.objects.filter(productvariantvalue__variant_id=variant_id)
            .distinct()
            .order_by("sort_order")
        )
        print(f"[DEBUG:get_queryset] SQL = {str(qs.query)}")
        return qs

    path_parameters = [
        OpenApiParameter(
            name="product_pk",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
            description="UUID of the parent Product",
        ),
        OpenApiParameter(
            name="variant_pk",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
            description="UUID of the parent Product Variant",
        ),
    ]

    @extend_schema(
        parameters=path_parameters,
        responses={200: ProductAttributeSerializer(many=True)},
        tags=["Product Attributes"],
        summary="List all attributes for a product variant",
    )
    def list(self, request, product_pk=None, variant_pk=None):
        print(f"[DEBUG:list] product_pk={product_pk}, variant_pk={variant_pk}")

        cursor = request.query_params.get("cursor") or "first"
        cache_key = f"{variant_pk}:{cursor}"
        print(f"[DEBUG:list] cache_key={cache_key}")

        cache_data = self.cache.get_results(cache_key)
        if cache_data:
            print("[DEBUG:list] Cache HIT")
            return ResponseFactory.success_collection(
                items=cache_data.get("items", []),
                pagination=cache_data.get("pagination", {}),
                message="Product attributes fetched successfully (cache)",
                status=status.HTTP_200_OK,
                request=request,
                cache="HIT",
            )

        print("[DEBUG:list] Cache MISS, hitting DB...")
        queryset = self.get_queryset()
        paginator = BaseCursorPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductAttributeSerializer(
            page, many=True, context={"request": request}
        )
        response_data = paginator.get_paginated_response_data(serializer.data)

        print(f"[DEBUG:list] items_count={len(response_data['items'])}")
        self.cache.cache_results(cache_key, response_data)

        return ResponseFactory.success_collection(
            items=response_data["items"],
            pagination=response_data["pagination"],
            message="Product attributes fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        parameters=path_parameters,
        responses={200: ProductAttributeSerializer},
        tags=["Product Attributes"],
    )
    def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
        print(
            f"[DEBUG:retrieve] product_pk={product_pk}, variant_pk={variant_pk}, pk={pk}"
        )

        attribute = get_object_or_404(self.get_queryset(), pk=pk)
        print(f"[DEBUG:retrieve] Found attribute -> {attribute}")

        serializer = ProductAttributeSerializer(attribute, context={"request": request})
        print(f"[DEBUG:retrieve] Serialized data -> {serializer.data}")

        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Product attribute fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )


# class ProductAttributeViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("product_attributes")

#     def get_queryset(self):
#         variant_id = self.kwargs.get("variant_pk")
#         return (
#             ProductAttribute.objects.filter(productvariantvalue__variant_id=variant_id)
#             .select_related()
#             .order_by("sort_order")
#         )

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
#         cursor = request.query_params.get("cursor") or "first"
#         cache_key = f"{variant_pk}:{cursor}"

#         cache_data = self.cache.get_results(cache_key)
#         if cache_data:
#             return ResponseFactory.success_collection(
#                 items=cache_data.get("items", []),
#                 pagination=cache_data.get("pagination", {}),
#                 message="Product attributes fetched successfully (cache)",
#                 status=status.HTTP_200_OK,
#                 request=request,
#                 cache="HIT",
#             )

#         queryset = self.get_queryset()
#         print("queryset -----------> ", queryset)
#         paginator = BaseCursorPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         print("before serializer page -----------> ", page)
#         serializer = ProductAttributeSerializer(
#             page, many=True, context={"request": request}
#         )
#         print("After serializer serialzer -----------> ", serializer)
#         response_data = paginator.get_paginated_response_data(serializer.data)
#         print("Response Data -----------> ", response_data)
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
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         print(" inside attribute retrieve method -----------> ", attribute)
#         serializer = ProductAttributeSerializer(attribute, context={"request": request})
#         print(" serializer data -----------> ", serializer.data)
#         print(f"pk - {pk}, product_pk - {product_pk}, variant_pk - {variant_pk}")
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={201: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#     )
#     def create(self, request, product_pk=None, variant_pk=None):
#         data = request.data.copy()
#         data["variant"] = variant_pk
#         serializer = ProductAttributeSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         self.cache.clear_prefix(variant_pk)
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute created successfully",
#             status=status.HTTP_201_CREATED,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={200: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#     )
#     def update(self, request, pk=None, product_pk=None, variant_pk=None):
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         serializer = ProductAttributeSerializer(
#             attribute, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         self.cache.clear_prefix(variant_pk)
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Product attribute updated successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=path_parameters, responses={204: None}, tags=["Product Attributes"]
#     )
#     def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
#         attribute = get_object_or_404(self.get_queryset(), pk=pk)
#         attribute.delete()

#         self.cache.clear_prefix(variant_pk)
#         return ResponseFactory.success_message(
#             message="Product attribute deleted successfully",
#             status=status.HTTP_204_NO_CONTENT,
#             request=request,
#         )


# # 4a3074b1-3cc3-4ae6-8081-114fef44fa68
# # b51480ce-7d8c-4c58-8a16-de5ff151c54f


# c4b225b1-27fd-4c49-aa93-7caa6ebd3962  variant id
#  b51480ce-7d8c-4c58-8a16-de5ff151c54f attribute id