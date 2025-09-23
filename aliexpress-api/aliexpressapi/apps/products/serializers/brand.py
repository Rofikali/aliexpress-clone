from rest_framework import serializers
from apps.products.models.brand import (
    Brand,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "description"]
