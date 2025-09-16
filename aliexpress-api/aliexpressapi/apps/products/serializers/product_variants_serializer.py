from rest_framework import serializers
from apps.products.models.product_variant_model import (
    ProductVariant,
)

from .product_attribute_serializer import ProductAttributeSerializer

class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "sku", "price", "stock", "attributes"]


