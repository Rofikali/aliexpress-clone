# new here
# apps.products/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models import (
    ProductVariant,
)
from apps.products.serializers.product_variants_serializer import (
    ProductVariantSerializer,
)


# apps.products/viewsets.py

# apps.products/viewsets.py


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
