# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# from apps.products.models.product_attribute_model import ProductAttribute
# from apps.products.serializers.product_attribute_serializer import (
#     ProductAttributeSerializer,
# )


# class ProductAttributeViewSet(viewsets.ViewSet):
#     """
#     Manage product attributes nested under variants.
#     """

#     def get_queryset(self):
#         variant_id = self.kwargs.get("variant_pk")
#         return ProductAttribute.objects.filter(variant_id=variant_id)

#     # Common parameters for all actions
#     path_parameters = [
#         OpenApiParameter(
#             name="product_pk",
#             type=OpenApiTypes.INT,
#             location=OpenApiParameter.PATH,
#             description="ID of the parent Product",
#         ),
#         OpenApiParameter(
#             name="variant_pk",
#             type=OpenApiTypes.INT,
#             location=OpenApiParameter.PATH,
#             description="ID of the parent Product Variant",
#         ),
#     ]

#     @extend_schema(
#         parameters=path_parameters,
#         responses={200: ProductAttributeSerializer(many=True)},
#         tags=["Product Attributes"],
#         summary="List all attributes for a product variant",
#         description="Retrieve all attributes belonging to a specific product variant.",
#     )
#     def list(self, request, product_pk=None, variant_pk=None):
#         queryset = self.get_queryset()
#         serializer = ProductAttributeSerializer(queryset, many=True)
#         return Response(serializer.data)

#     @extend_schema(
#         parameters=path_parameters,
#         responses={200: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#         summary="Retrieve a single attribute",
#         description="Retrieve a single attribute by its ID for a given product variant.",
#     )
#     def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
#         try:
#             attribute = self.get_queryset().get(pk=pk)
#         except ProductAttribute.DoesNotExist:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProductAttributeSerializer(attribute)
#         return Response(serializer.data)

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={201: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#         summary="Create a new attribute",
#         description="Create a new attribute for a specific product variant.",
#     )
#     def create(self, request, product_pk=None, variant_pk=None):
#         data = request.data.copy()
#         data["product"] = product_pk
#         data["variant"] = variant_pk
#         serializer = ProductAttributeSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#         parameters=path_parameters,
#         request=ProductAttributeSerializer,
#         responses={200: ProductAttributeSerializer},
#         tags=["Product Attributes"],
#         summary="Update an attribute",
#         description="Update an existing attribute (full or partial update).",
#     )
#     def update(self, request, pk=None, product_pk=None, variant_pk=None):
#         try:
#             attribute = self.get_queryset().get(pk=pk)
#         except ProductAttribute.DoesNotExist:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ProductAttributeSerializer(
#             attribute, data=request.data, partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#         parameters=path_parameters,
#         responses={204: None},
#         tags=["Product Attributes"],
#         summary="Delete an attribute",
#         description="Delete an attribute by ID from a product variant.",
#     )
#     def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
#         try:
#             attribute = self.get_queryset().get(pk=pk)
#         except ProductAttribute.DoesNotExist:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

#         attribute.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# apps/products/views/product_attribute_viewset.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.shortcuts import get_object_or_404

from apps.products.models.product_attribute_model import ProductAttribute
from apps.products.serializers.product_attribute_serializer import ProductAttributeSerializer


class ProductAttributeViewSet(viewsets.ViewSet):
    def get_queryset(self):
        variant_id = self.kwargs.get("variant_pk")
        return ProductAttribute.objects.filter(variant_id=variant_id)

    # common params for docs
    path_parameters = [
        OpenApiParameter(
            name="product_pk", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
            description="ID of the parent Product",
        ),
        OpenApiParameter(
            name="variant_pk", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
            description="ID of the parent Product Variant",
        ),
    ]

    @extend_schema(
        parameters=path_parameters,
        responses={200: ProductAttributeSerializer(many=True)},
        tags=["Product Attributes"],
        summary="List all attributes for a product variant",
    )
    def list(self, request, product_pk=None, variant_pk=None):
        queryset = self.get_queryset()
        serializer = ProductAttributeSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=path_parameters,
        responses={200: ProductAttributeSerializer},
        tags=["Product Attributes"],
        summary="Retrieve a single attribute",
    )
    def retrieve(self, request, pk=None, product_pk=None, variant_pk=None):
        attribute = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ProductAttributeSerializer(attribute)
        return Response(serializer.data)

    @extend_schema(
        parameters=path_parameters,
        request=ProductAttributeSerializer,
        responses={201: ProductAttributeSerializer},
        tags=["Product Attributes"],
        summary="Create a new attribute",
    )
    def create(self, request, product_pk=None, variant_pk=None):
        data = request.data.copy()
        data["product"] = product_pk
        data["variant"] = variant_pk
        serializer = ProductAttributeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=path_parameters,
        request=ProductAttributeSerializer,
        responses={200: ProductAttributeSerializer},
        tags=["Product Attributes"],
        summary="Update an attribute",
    )
    def update(self, request, pk=None, product_pk=None, variant_pk=None):
        attribute = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ProductAttributeSerializer(attribute, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        parameters=path_parameters,
        responses={204: None},
        tags=["Product Attributes"],
        summary="Delete an attribute",
    )
    def destroy(self, request, pk=None, product_pk=None, variant_pk=None):
        attribute = get_object_or_404(self.get_queryset(), pk=pk)
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
