from rest_framework import serializers
from apps.products.models import (
    ProductImage,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]
