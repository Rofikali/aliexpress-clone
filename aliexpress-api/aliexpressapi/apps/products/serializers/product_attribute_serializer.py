from rest_framework import serializers
from apps.products.models import (
    ProductAttribute,
)


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]
