# # # new here
# # # apps.products/viewsets.py
# # from rest_framework.viewsets import ViewSet
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.shortcuts import get_object_or_404

# # from drf_spectacular.utils import extend_schema

# # from apps.products.models import (
# #     ProductVariant,
# # )
# # from apps.products.serializers.product_variants_serializer import (
# #     ProductVariantSerializer,
# # )


# # # -------------------- VARIANTS --------------------
# # class ProductVariantViewSet(ViewSet):
# #     @extend_schema(
# #         responses={200: ProductVariantSerializer(many=True)},
# #         tags=["Product Variants"],
# #     )
# #     def list(self, request):
# #         queryset = ProductVariant.objects.all()
# #         serializer = ProductVariantSerializer(queryset, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #     @extend_schema(
# #         responses={200: ProductVariantSerializer},
# #         tags=["Product Variants"],
# #     )
# #     def retrieve(self, request, pk=None):
# #         variant = get_object_or_404(ProductVariant, id=pk)
# #         serializer = ProductVariantSerializer(variant)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# # apps/products/viewsets/product_variants_viewset.py
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema

# from apps.products.models.product_variant_model import ProductVariant
# from apps.products.serializers.product_variants_serializer import (
#     ProductVariantSerializer,
# )


# class ProductVariantViewSet(ViewSet):
#     # route_name = "product-variants"  # will map to /products/:id/variants

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
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @extend_schema(
#         responses={200: ProductVariantSerializer},
#         tags=["Product Variants"],
#         summary="Retrieve single product variant",
#     )
#     def retrieve(self, request, pk=None, product_pk=None):
#         variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
#         serializer = ProductVariantSerializer(variant)
#         return Response(serializer.data, status=status.HTTP_200_OK)



# apps/products/views/product_variants_viewset.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from apps.products.models.product_variant_model import ProductVariant
from apps.products.serializers.product_variants_serializer import ProductVariantSerializer


class ProductVariantViewSet(ViewSet):
    def get_queryset(self, product_id=None):
        qs = ProductVariant.objects.all()
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

    @extend_schema(
        responses={200: ProductVariantSerializer(many=True)},
        tags=["Product Variants"],
        summary="List product variants",
    )
    def list(self, request, product_pk=None):
        queryset = self.get_queryset(product_pk)
        serializer = ProductVariantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: ProductVariantSerializer},
        tags=["Product Variants"],
        summary="Retrieve single product variant",
    )
    def retrieve(self, request, pk=None, product_pk=None):
        variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)
