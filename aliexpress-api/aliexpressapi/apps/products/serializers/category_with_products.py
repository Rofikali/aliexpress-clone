# apps/products/serializers/category_with_products.py
from rest_framework import serializers
from apps.products.models.category import Category
from apps.products.serializers.product import ProductSerializer


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    # products = serializers.SerializerMethodField()
    category_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "category_products"]

    # def get_products(self, obj):
    #     products = obj.product_set.all().order_by("-created_at")
    #     return ProductSerializer(products, many=True, context=self.context).data
