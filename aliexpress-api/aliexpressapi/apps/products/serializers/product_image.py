from rest_framework import serializers
from apps.products.models.product_images import (
    ProductImages,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ["id", "product", "image"]
