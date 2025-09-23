# apps/home/serializers/section_product_serializer.py
from rest_framework import serializers
from apps.home.models.section_product import HomepageProduct
from apps.products.serializers.product import ProductSerializer


class HomepageProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, context={"request": None})

    class Meta:
        model = HomepageProduct
        fields = ["id", "product", "sort_order"]
