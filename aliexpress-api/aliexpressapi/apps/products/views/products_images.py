# new here
# apps.products/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models.product_images import (
    ProductImages,
)
from apps.products.serializers.product_image import (
    ProductImageSerializer,
)



# apps.products/viewsets.py

# apps.products/viewsets.py


# -------------------- PRODUCT IMAGES --------------------
class ProductImageViewSet(ViewSet):
    @extend_schema(
        responses={200: ProductImageSerializer(many=True)},
        tags=["Product Images"],
    )
    def list(self, request):
        queryset = ProductImages.objects.all()
        serializer = ProductImageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: ProductImageSerializer},
        tags=["Product Images"],
    )
    def retrieve(self, request, pk=None):
        image = get_object_or_404(ProductImages, id=pk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
